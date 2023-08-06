import os
import re
import types
import base64
import inspect
import logging
import traceback
import dill
from six.moves.urllib import parse as urlparse
from localstack.utils import persistence
from localstack.utils.common import to_str, to_bytes, mkdir

# List of mapping rules that identify IDs or generated values that need
# to be adjusted/replaced when replaying recorded API calls.
CONTENT_MAPPINGS = [{
    'src': {
        'api': 'sns',
        'method': 'POST',
        'candidate_extractor': r'.*Action=([^&]+).*',
        'candidate_matcher': r'Subscribe',
        'id_extractor': r'.*<SubscriptionArn>\s*([^<]+)\s*</SubscriptionArn>.*'
    },
    'tgt': {}
}]
# maps extracted IDs: (originally recorded ID) -> (newly generated ID)
CONTENT_IDS = {}

IMPLEMENTED_PERSISTENCE_APIS = ['iam', 'sqs', 's3']

LOG = logging.getLogger(__name__)


def replace_extracted_ids(api, data, reverse=False):
    try:
        data = to_str(data or '')
        is_str = True
    except Exception:
        data = to_bytes(data or '')
        is_str = False
    for recorded, actual in CONTENT_IDS.items():
        if reverse:
            # swap
            tmp = recorded
            recorded = actual
            actual = tmp
        if not is_str:
            recorded, actual = to_bytes(recorded), to_bytes(actual)
        data = data.replace(recorded, actual)
    return data


def transform_incoming_data(api, data, url_encoded=False):
    """ Transform the payload of incoming data - replacing recorded (old) with actual (new) IDs. """
    if url_encoded:
        data = urlparse.parse_qs(to_str(data))
        data = dict([(k, v[0]) for k, v in data.items()])
        for k, value in data.items():
            data[k] = replace_extracted_ids(api, value)
        data = urlparse.urlencode(data)
        return data
    return replace_extracted_ids(api, data)


def transform_outgoing_data(api, response):
    """ Transform the payload of outgoing data - replacing actual (new) with recorded (old) IDs. """
    response._content = replace_extracted_ids(api, response._content, reverse=True)
    response.headers['Content-Length'] = str(len(response._content))


def extract_id_mappings(command, received_response):
    """ Extract any ID mappings from the given API response """

    api = command['a']
    method = command['m']

    request_data = None
    recorded_response = None
    actual_response = None

    for map in CONTENT_MAPPINGS:
        src = map['src']
        if src.get('api') not in [None, api] or src.get('method') not in [None, method]:
            continue
        try:
            request_data = request_data or to_str(base64.b64decode(command.get('d')))
            recorded_response = recorded_response or to_str(base64.b64decode(command.get('rd')))
            actual_response = actual_response or to_str(received_response.content)
        except Exception:
            return
        candidate_value = re.sub(src['candidate_extractor'], r'\1', request_data)
        if not re.match(candidate_value, src['candidate_matcher']):
            return
        recorded_id = re.sub(src['id_extractor'], r'\1', recorded_response)
        actual_id = re.sub(src['id_extractor'], r'\1', actual_response)
        # keep a reference to the recorded/actual IDs, IF they were extracted successfully
        if recorded_id != recorded_response and actual_id != actual_response:
            CONTENT_IDS[recorded_id] = actual_id


def enable_extended_persistence():
    def record(api, method=None, path=None, data=None, headers=None, response=None, request=None):
        if api in IMPLEMENTED_PERSISTENCE_APIS:
            return

        if api in ['sns']:
            if method in ['GET']:
                return

        record_orig(api, method, path, data, headers, response, request)

    record_orig = persistence.record
    persistence.record = record

    def replay_command(command):
        if command['a'] in IMPLEMENTED_PERSISTENCE_APIS:
            return

        response = replay_command_orig(command)
        extract_id_mappings(command, response)
        return response

    def prepare_replay_data(command):
        data = prepare_replay_data_orig(command)
        data = replace_extracted_ids(command['a'], data)
        return data

    replay_command_orig = persistence.replay_command
    persistence.replay_command = replay_command
    prepare_replay_data_orig = persistence.prepare_replay_data
    persistence.prepare_replay_data = prepare_replay_data


def load_backend_state(state_dir):
    mkdir(state_dir)

    for dir_path, _, files in os.walk(state_dir):
        for key in files:
            region = os.path.basename(dir_path)
            path = os.path.join(state_dir, region, key)
            restored = load_persisted_object(path)
            if restored is not None:
                yield key, region, restored


def persist_state(state_dir, region, partition, state, rwlock):
    excluded_class_attributes = ['REGIONS']
    with rwlock.gen_wlock():
        region_dir = os.path.join(state_dir, region)
        mkdir(region_dir)
        path = os.path.join(region_dir, partition)
        if inspect.isclass(state):
            state = {k: v for k, v in state.__dict__.items()
                if k not in excluded_class_attributes and not k.startswith('_') and not isinstance(v, property)}
        try:
            persist_object(state, path)
        except Exception as e:
            LOG.info('Unable to persist backend state to path %s: %s %s' % (path, e, traceback.format_exc()))


def load_persisted_object(state_file):
    if not os.path.isfile(state_file):
        return

    with open(state_file, 'rb') as f:
        try:
            return dill.loads(f.read())
        except Exception as e:
            LOG.debug('Unable to read pickled persistence file %s: %s' % (state_file, e))


def persist_object(obj, state_file):
    with open(state_file, 'wb') as f:
        return f.write(dill.dumps(obj))


def patch_pickle_lib():
    # Apply a patch to the pickle lib to avoid errors like:
    #   "TypeError: cannot pickle 'generator' object"
    def save_dict(self, obj, *args, **kwargs):
        def is_gen(o):
            return isinstance(o, types.GeneratorType) or inspect.isgeneratorfunction(o)
        if isinstance(obj, dict):
            has_generator = any(is_gen(o) for o in obj.values())
            if has_generator:
                obj = {k: v for k, v in obj.items() if not is_gen(v)}
        return save_dict_orig(self, obj, *args, **kwargs)
    import pickle
    save_dict_orig = pickle._Pickler.save_dict
    pickle._Pickler.save_dict = save_dict


patch_pickle_lib()
