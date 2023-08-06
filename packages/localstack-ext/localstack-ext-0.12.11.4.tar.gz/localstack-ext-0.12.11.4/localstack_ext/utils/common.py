import re
import time
import asyncio
import logging
import threading
import collections
from cachetools import TTLCache
from collections import defaultdict
from localstack import config
from localstack.utils.common import (
    TMP_THREADS, FuncThread, ShellCommandThread, run, to_str, in_docker, rm_docker_container, port_can_be_bound)
from localstack_ext import config as ext_config

LOG = logging.getLogger(__name__)

# event loop initialized in the main thread on import
EVENT_LOOP = asyncio.get_event_loop()
EVENT_LOOP_STARTED = False

# cache for locally available ports
PORTS_CACHE = TTLCache(maxsize=100, ttl=7)
PORTS_LOCK = threading.RLock()

ITERABLE_TYPES = (list, set, tuple)


class OrderedSet(collections.abc.MutableSet):
    """ Ordered, hashable set - based on http://code.activestate.com/recipes/576694 """

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, OrderedSet):
            if not isinstance(other, ITERABLE_TYPES):
                return other in self
        return len(self) == len(other) and set(self) == set(other)

    def __hash__(self):
        return sum([hash(e) for e in self])


class MultiKeyDict(dict):

    class AliasValueConflict(Exception):
        pass

    class MultiKey(object):
        def __init__(self):
            self.values = OrderedSet()
            self._hash = None

        def add_value(self, value):
            self.values.add(value)
            self._hash = None

        def remove_value(self, value):
            self.values.remove(value)
            self._hash = None

        def __eq__(self, other):
            other_values = other.values if isinstance(other, MultiKeyDict.MultiKey) else other
            return self.values == other_values

        def __hash__(self):
            if self._hash is None:
                # cache the hash value for slight performance benefit (TODO needed/remove?)
                self._hash = hash(self.values)
            return self._hash

        def __repr__(self):
            return 'MultiKey(%s)' % list(self.values)

    def get(self, key, default=None, *args):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __contains__(self, key):
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key, *args):
        k, v = self._get_item(key)
        if k:
            return v
        raise KeyError(key)

    def __setitem__(self, key, value, *args):
        k, v = self._get_item(key)
        if not k:
            k = self.MultiKey()
            k.add_value(key)
        super(MultiKeyDict, self).__setitem__(k, value, *args)

    def _get_item(self, key):
        for k, v in self.items():
            if key == k or key in k.values:
                return k, v
        return None, None

    def pop(self, key, *args, **kwargs):
        k1, v1 = self._get_item(key)
        if not k1:
            if not len(args) and 'default' not in kwargs:
                raise KeyError(key)
            return args[0] if len(args) else kwargs.get('default')
        return super(MultiKeyDict, self).pop(k1)

    def set_alias(self, one, other, force_remap=False):
        k1, v1 = self._get_item(one)
        k2, v2 = self._get_item(other)
        if not k1 and not k2:
            raise KeyError([one, other])
        if k1 and k2:
            if v1 != v2:
                if force_remap:
                    return self._remap_aliases(one, other)
                raise self.AliasValueConflict(
                    'Different existing values for alias keys "%s"/"%s": "%s" != "%s"' % (k1, k2, v1, v2))
            if k1 != k2:
                self.pop(other)
        k1 and self._add_key_alias(k1, other)
        k2 and self._add_key_alias(k2, one)

    def _remap_aliases(self, one, other):
        k1, v1 = self._get_item(one)
        k2, v2 = self._get_item(other)
        if k1 == k2:
            raise Exception('Attribute keys "%s" and "%s" are already aliased, no need to remap' % (one, other))
        self._remove_key_alias(k2, other)
        self._add_key_alias(k1, other)

    def _remove_key_alias(self, key_obj, alias):
        """ Remove an alias from the given key, then re-index the entry (for updated key hash) """
        value = self.pop(key_obj)
        key_obj.remove_value(alias)
        super(MultiKeyDict, self).__setitem__(key_obj, value)

    def _add_key_alias(self, key_obj, alias):
        """ Add an alias to the given key, then re-index the entry (for updated key hash) """
        value = self.pop(key_obj)
        key_obj.add_value(alias)
        super(MultiKeyDict, self).__setitem__(key_obj, value)


class DockerRunThread(ShellCommandThread):
    def __init__(self, cmd, container_name=None, **kwargs):
        super(DockerRunThread, self).__init__(cmd, params={}, **kwargs)
        self.container_name = container_name

    def stop(self, quiet=False):
        super(DockerRunThread, self).stop(quiet=quiet)
        if self.container_name:
            rm_docker_container(self.container_name)


def get_docker_container_logs(container_name_or_id):
    try:
        return run('%s logs %s' % (config.DOCKER_CMD, container_name_or_id), print_error=False)
    except Exception:
        return ''


# TODO: merge with async_utils.py upstream?
def run_coroutine_in_event_loop(coroutine):
    start_async_event_loop()
    return asyncio.run_coroutine_threadsafe(coroutine, EVENT_LOOP)


def start_async_event_loop(loop=None):
    loop = loop or EVENT_LOOP

    global EVENT_LOOP_STARTED
    if EVENT_LOOP_STARTED:
        return loop

    def run_broker(*args):
        loop.run_forever()

    thread = FuncThread(run_broker)
    thread.start()
    TMP_THREADS.append(thread)
    EVENT_LOOP_STARTED = True
    time.sleep(1)
    return loop


def get_available_service_instance_port():
    ports_range = range(ext_config.SERVICE_INSTANCES_PORTS_START, ext_config.SERVICE_INSTANCES_PORTS_END)
    with PORTS_LOCK:
        for port in ports_range:
            if not PORTS_CACHE.get(port) and port_can_be_bound(port):
                # reserve the port for a short period of time
                PORTS_CACHE[port] = '__reserved__'
                return port
    raise Exception('No free network ports available to start service instance: %s' % list(PORTS_CACHE.keys()))


class alldefaultdict(defaultdict):
    def __contains__(self, item):
        return True

    def get(self, key, default=None):
        return self[key]


# TODO move to upstream common.py!
def assign_to_path(target, path, value):
    path = path.split('.')
    for i in range(len(path) - 1):
        target_new = target[path[i]] = target.get(path[i], {})
        target = target_new
    target[path[-1]] = value


def get_docker_image_names(include_tags=True):
    format = '{{.Repository}}:{{.Tag}}' if include_tags else '{{.Repository}}'
    output = to_str(run("docker images --format '%s'" % format))
    images = re.split(r'\s+', output.strip().replace('\n', ' '))
    images = [img for img in images if '<none>' not in img]
    return set(images)


def is_docker_image_pulled(image_name):
    images = get_docker_image_names()
    return image_name in images or '%s:latest' % image_name in images


def get_docker_container_host(container_name=None):
    # TODO: lookup container IP from container name?
    return config.DOCKER_HOST_FROM_CONTAINER if in_docker() else config.LOCALSTACK_HOSTNAME
