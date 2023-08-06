import re
import json
import logging
import xmltodict
from localstack.utils.common import to_str, is_sub_dict
from localstack_ext.services.azure import api_specs, azure_utils
from localstack_ext.services.azure.api_handlers import (
    TenantMetadata, SourceControl, ResourceGraph, EventHubs, EventHubNamespaces,
    EventHubAuthRules, EventHubConsumerGroups)

LOG = logging.getLogger(__name__)

# default regex flags
REGEX_FLAGS = re.DOTALL | re.IGNORECASE

# list of APIs that need to be matched against a separate resource tree
APIS_WITH_SEPARATE_RESOURCE_TREE = ['storage-queue', 'tenant-discovery', 'resource-groups']
APIS_WITHOUT_SPECS = ['tenant-discovery', 'scm']


class RequestContext(object):
    def __init__(self, method, path, data, headers, api=None):
        self.method = method
        self.path = path
        self.data = data
        self.headers = headers
        self.api = api
        # path to match against path pattern after customizations applied
        self.path_to_match = path
        # maps path keys to path parameter values
        self.path_params = None
        # instance of APISpec that contains spec details of the target API method
        self.spec = None

    def get_path_params(self):
        if self.path_params is not None:
            return self.path_params
        self.path_params = {}
        if not self.spec:
            return self.path_params
        path_pattern = self.spec.path_pattern
        params = re.findall(r'{(\w+)}', path_pattern)
        regex = re.sub(r'{(\w+)}', r'([^\?]+)', path_pattern).replace('?', r'\?')
        matches = re.match(regex, self.path_to_match)
        if matches:
            param_values = matches.groups()
            if len(params) == len(param_values):
                self.path_params = dict(zip(params, param_values))
        else:
            LOG.info('Unable to match pattern "%s" to path: %s' % (regex, self.path))
        return self.path_params

    def content(self):
        try:
            content = to_str(self.data or '')
            if content.startswith('<'):
                return xmltodict.parse(content)
            if content.startswith('{'):
                try:
                    return json.loads(content)
                except Exception:
                    import dirtyjson
                    return dirtyjson.loads(content)
        except Exception as e:
            LOG.info('Unable to parse request payload: %s - %s' % (content, e))
            raise
        return content

    def host(self):
        return self.headers.get('host', 'localhost')

    def path_without_query(self):
        return self.path.split('?')[0]

    def spec_path_without_query(self):
        return (self.spec.path_pattern or '').split('?')[0]

    def get_query_params(self):
        _, _, params = self.path.partition('?')
        return azure_utils.parse_qs(params)


class ResourceTree(object):
    API_TREES = {}

    def __init__(self, api_key):
        self.api_key = api_key
        self.root = ResourceNode()

    def add_path(self, path, value):
        parts = PathPart.split_path(path)
        node = self.root_node()
        for part in parts:
            node = node.insert_child(part)
        if node.value and node.value != value:
            raise Exception('Existing node %s for path %s when inserting %s' % (node.value, path, value))
        node.value = value

    def match(self, path, query_params={}):
        node = self.root_node()
        path_parts = PathPart.split_path(path)
        result = node.find_descendants(path_parts)
        if not result:
            raise Exception('Unable to find matching patterns for API "%s", path: %s' % (self.api_key, path))
        if len(result) > 1:
            raise Exception('Ambiguous path "%s" - found %s matching path patterns: %s' % (
                path, len(result), result))
        return result[0]

    def root_node(self):
        self.root = self.root or ResourceNode()
        return self.root

    @staticmethod
    def get(api=None):
        key = api if api in APIS_WITH_SEPARATE_RESOURCE_TREE else '_default_'
        trees = ResourceTree.API_TREES
        result = trees[key] = trees.get(key) or ResourceTree(key)
        return result


class ResourceNode(object):
    def __init__(self):
        # maps path parts to outgoing edges
        # TODO: convert to list or set (currently maps PathPart to itself)
        self.out = {}
        # holds the value of this node
        self.value = None

    def insert_child(self, path_part, query_params={}):
        edges = self.get_outgoing(path_part, query_params=query_params, exact_match=True)
        edge = edges and edges[0]
        if not edge:
            child = ResourceNode()
            edge = PathPart.get(path_part, query_params=query_params, target=child)
            self.out[path_part] = edge
        return edge.target

    def find_descendants(self, path_parts, result_list=None, query_params={}):
        result_list = [] if result_list is None else result_list
        # path_parts, params = PathPart.split_path(path_parts)
        if not path_parts:
            result_list.append(self)
            return result_list
        path_part = path_parts[0]
        query_params = query_params if len(path_parts) == 1 else {}
        children = self.get_outgoing(path_part, query_params=query_params)
        if not children:
            if self.value and path_part.is_query_param_node():
                # this case can happen for requests like /queue-6d2021e0/messages?numofmessages=5
                # where the matching API spec route is /{queueName}/messages (without query params)
                result_list.append(self)
                return result_list
        for child in children or []:
            child.target.find_descendants(path_parts[1:], result_list=result_list, query_params=query_params)
        return result_list

    def get_outgoing(self, path_part, query_params={}, exact_match=False):
        path_part = PathPart.get(path_part, query_params=query_params)
        query_params = path_part.query_params
        direct_match = self.out.get(path_part)
        if direct_match:
            return [direct_match]
        candidates = [e for e in self.out.values() if e.is_wildcard()]
        if not path_part.value:
            candidates = [e for e in self.out.values() if e.is_query_param_node()]
        if exact_match:
            candidates = [n for n in candidates if n.query_params == query_params]
        else:
            candidates = [n for n in candidates if is_sub_dict(n.query_params, query_params)]
        return candidates

    def __repr__(self):
        return 'Node(%s)' % self.value


class PathPart(object):
    def __init__(self, value, query_params={}, target=None):
        value, _, params = value.partition('?')
        self.value = value
        self.target = target
        self.query_params = query_params or azure_utils.parse_qs(params)

    @staticmethod
    def split_path(path):
        if isinstance(path, list):
            return path
        path, _, query_string = path.partition('?')
        params = azure_utils.parse_qs(query_string)
        path_parts = path.replace('//', '/').strip('/').split('/')
        path_parts = [PathPart(p) for p in path_parts]
        if params:
            path_parts.append(PathPart('', query_params=params))
        return path_parts

    @staticmethod
    def get(part, query_params={}, target=None):
        if not isinstance(part, PathPart):
            part = PathPart(part, query_params=query_params)
        part.target = target
        return part

    def __eq__(self, other):
        value = other
        query_params = {}
        if isinstance(other, PathPart):
            value = other.value
            query_params = other.query_params
        value_lower1 = (self.value or '').lower()
        value_lower2 = (value or '').lower()
        if value_lower1 != value_lower2:
            return False
        result = self.query_params_match(query_params)
        return result

    def __hash__(self):
        # force full object comparison to enable wildcard matches
        return 0

    def is_wildcard(self, value=None):
        value = self.value if value is None else value
        return re.match(r'^\{[^}]+\}$', value)

    def query_params_match(self, query_params):
        params1 = query_params or {}
        params2 = self.query_params or {}
        if params1.keys() != params2.keys():
            return False
        for key, value1 in params1.items():
            value2 = params2.get(key)
            if value1 != value2 and not self.is_wildcard(value1) and not self.is_wildcard(value2):
                return False
        return True

    def is_query_param_node(self):
        return not self.value and self.query_params

    def __repr__(self):
        return 'PathPart("%s",%s)' % (self.value, self.query_params)


def get_resource_tree(api_name=None):
    if not ResourceTree.API_TREES:
        all_specs = api_specs.load_all_api_specs()
        inserted = []
        for api, specs in all_specs.items():
            api_tree = ResourceTree.get(api)
            paths = specs.get_path_candidates()
            for path, details in paths.items():
                value = {}
                for method, method_details in details.items():
                    value[method] = api_specs.APITarget(method, path, method_details)
                api_tree.add_path(path, value)
                inserted.append(path)
        LOG.info('Parsed and inserted API specs for %s resource paths' % len(inserted))
    return ResourceTree.get(api_name)


def prepare_path_to_match(req):
    req.path_to_match = req.path
    if req.path_to_match.startswith('/storage-blob/'):
        req.path_to_match = req.path_to_match[len('/storage-blob'):]
    if req.api == 'storage-blob' and req.method == 'PUT' and '?' not in req.path:
        req.path_to_match = '%s?BlockBlob' % req.path_to_match
    if req.api == 'storage-queue':
        req.path_to_match = '/%s' % req.path_to_match.lstrip('/').partition('/')[2]


def load_api_spec_for_request(req):
    if req.api in APIS_WITHOUT_SPECS:
        return
    tree = get_resource_tree(req.api)
    query_params = req.get_query_params()
    specs = tree.match(req.path_to_match, query_params=query_params)
    if not specs:
        LOG.info('Unable to find specs for API "%s", request: %s %s' % (req.api, req.method, req.path))
        return
    req.spec = specs.value.get(req.method.lower())
    return req.spec


def determine_api(method, path, headers):
    """ Apply a couple of heuristics to determine the target API. """
    agent = headers.get('User-Agent', '')
    host = headers.get('Host', '')
    api = '_unknown_'
    if 'storage-queue' in agent:
        # TODO: find a more robust way to determine the target! (avoid using User-Agent)
        api = 'storage-queue'
    elif '/providers/Microsoft.Web/sites' in path:
        api = 'web-apps'
    elif '/providers/Microsoft.Web/serverfarms' in path:
        api = 'service-plans'
    elif '/providers/Microsoft.Web/' in path:
        api = 'web-resources'
    elif '/providers/Microsoft.Storage' in path:
        api = 'storage-accounts'
    elif '/Microsoft.ServiceBus/' in path:
        api = 'servicebus'
    elif re.match(r'.*/providers/Microsoft.EventHub/namespaces/.*/authorizationRules.*', path, flags=REGEX_FLAGS):
        return EventHubAuthRules.api()
    elif re.match(r'.*/providers/Microsoft.EventHub/namespaces/.*/consumergroups.*', path, flags=REGEX_FLAGS):
        return EventHubConsumerGroups.api()
    elif re.match(r'.*/providers/Microsoft.EventHub/namespaces/.*/eventhubs.*', path, flags=REGEX_FLAGS):
        return EventHubs.api()
    elif re.match(r'.*/providers/Microsoft.EventHub/namespaces.*', path, flags=REGEX_FLAGS):
        return EventHubNamespaces.api()
    elif '/providers/Microsoft.ResourceGraph/resources' in path:
        return ResourceGraph.api()
    elif path.startswith('/common/discovery/instance'):
        return TenantMetadata.api()
    elif path.startswith('/common/UserRealm/'):
        return TenantMetadata.api()
    elif '/oauth2/' in path or '/.well-known/' in path:
        return TenantMetadata.api()
    elif re.match('.*/providers/microsoft.insights/components.*', path, flags=REGEX_FLAGS):
        return 'appinsights-components'
    elif re.match(r'.*/providers/microsoft.insights/.*', path, flags=REGEX_FLAGS):
        return 'resource-groups'
    elif re.match(r'^/subscriptions.*/resourcegroups.*', path, flags=REGEX_FLAGS):
        return 'resource-groups'
    elif re.match(r'^/(subscriptions|tenants)(\?|$)', path, flags=REGEX_FLAGS):
        return TenantMetadata.api()
    elif path == '/arm/cloud/metadata':
        return TenantMetadata.api()
    elif '.scm.' in host or re.match('/api/(settings|deployments|zipdeploy).*', path):
        return SourceControl.api()
    else:
        api = path.lstrip('/').split('/')[0]
    if api not in api_specs.SPECS:
        LOG.warning('Unable to extract API specifier (%s) from request: %s %s %s' % (api, method, path, dict(headers)))
    return api
