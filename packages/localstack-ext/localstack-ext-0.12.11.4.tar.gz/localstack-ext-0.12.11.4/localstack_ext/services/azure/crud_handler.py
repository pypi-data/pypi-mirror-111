import re
import json
import logging
from requests.structures import CaseInsensitiveDict
from localstack.utils.common import short_uid, epoch_timestamp
from localstack.utils.aws.aws_responses import requests_response
from localstack_ext.services.azure.azure_utils import log

LOG = logging.getLogger(__name__)

# maps resource_type -> resource_id -> details
RESOURCES = {}


def handle_request_for_method(req):
    if not req.spec or not is_crud_operation(req.spec.method_details):
        log('Unable to determine CRUD operation for %s %s' % (req.method, req.path))
        return
    result = handle_request(req)
    return result


def post_resource(req, spec, responses):
    return create_resource(req, spec, responses)


def create_resource(req, spec, responses):
    responses = responses or {}
    map = _resource_map(spec.resource_type)
    resource_id = extract_id_from_path(req)
    data = req.content()
    if not req.data:
        data = {}

    if not isinstance(data, dict):
        LOG.info('Unable to extract payload from request %s %s: %s' % (req.method, req.path, data))
    else:
        data['id'] = data.get('id') or resource_id
        resource_name = extract_name_from_path(req) or short_uid()
        data['name'] = data.get('name') or resource_name

    # store a reference to the payload data
    map[resource_id] = data

    status = 200
    result = construct_response(status, data=data, responses=responses)

    return result


def update_resource(req, spec, responses):
    responses = responses or {}
    map = _resource_map(spec.resource_type)
    data = req.content()
    resource_id = extract_id_from_path(req) or data.get('id')

    status = 200
    existing = map.get(resource_id)
    if existing is not None:
        recursive_merge(existing, data)
    else:
        status = 404

    result = construct_response(status, data=existing, responses=responses)

    return result


def read_resource(req, spec, responses=None):
    map = _resource_map(spec.resource_type)
    resource_id = extract_id_from_path(req)
    resource_name = extract_name_from_path(req)

    status = 200
    details = []

    if resource_name:
        details = map.get(resource_id)
        if details is None:
            LOG.debug('Unable to find "%s" in IDs for resource type "%s": %s' % (
                resource_id, spec.resource_type, list(map.keys())))
            status = 404
            details = {}
    else:
        details = {'value': list(map.values())}

    response = construct_response(status, data=details, responses=responses)
    adjust_response_for_range_header(req.headers, response)

    return response


def delete_resource(req, spec, responses=None):
    map = _resource_map(spec.resource_type)
    resource_id = extract_id_from_path(req)
    if resource_id not in map:
        return 404
    details = map.pop(resource_id)

    status = 202
    response = construct_response(status, data=details, responses=responses)

    return response


def handle_request(req):
    spec = req.spec
    spec.resource_type = get_resource_type(req, spec)
    responses = spec.method_details.get('responses', {})
    if not spec.resource_type:
        return
    if req.method == 'PUT':
        result = create_resource(req, spec, responses=responses)
    elif req.method == 'POST':
        result = post_resource(req, spec, responses=responses)
    elif req.method == 'PATCH':
        result = update_resource(req, spec, responses=responses)
    elif req.method == 'GET':
        result = read_resource(req, spec, responses=responses)
    elif req.method == 'DELETE':
        result = delete_resource(req, spec, responses=responses)
    return result


# ---------------
# UTIL FUNCTIONS
# ---------------

def construct_response(status, data=None, responses={}):
    # look up response
    response = responses.get(str(status))
    if not response:
        if status == 200 and responses.get(str(201)):
            # for certain create operations, we need to report status code 201
            status = 201
        else:
            LOG.info('Unable to find status code %s in response codes: %s' % (status, list(responses.keys())))
    headers = {}
    headers['Date'] = epoch_timestamp()

    # TODO replace mock data with real values!
    headers['Content-MD5'] = 'sQqNsWTgdUEFt6mb5y4/5Q=='
    # headers['x-ms-content-crc64'] = '77uWZTolTHU'
    headers['ETag'] = '0x8CB171BA9E94B0B'

    if isinstance(data, (dict, list)):
        data = json.dumps(data)
    result = requests_response(data, status_code=status, headers=headers)
    return result


def adjust_response_for_range_header(headers, response):
    range = headers.get('X-Ms-Range', '')
    if not range.startswith('bytes='):
        return
    start, end = range.split('bytes=')[-1].split('-')
    content = response.content or ''
    start = int(start)
    if len(content) <= start:
        return
    end = min(len(content), int(end))
    response._content = content[start:end]
    response.headers['Content-Range'] = 'bytes %s-%s/%s' % (start, end, len(content))


def recursive_merge(target, source):
    if isinstance(source, dict):
        target = {} if target is None else target
        for k, v in source.items():
            target[k] = recursive_merge(target.get(k), source[k])
        return target
    return source


def get_resource_type(req, spec):
    result = re.sub(r'.*restype=([^&]+).*', r'\1', spec.path_pattern)
    if result != spec.path_pattern:
        return result
    # return default resource types
    if req.api == 'storage-blob':
        return 'blob'
    if req.api == 'storage-queue':
        return 'queue'
    if req.api == 'web-apps' and 'Microsoft.Web/sites' in req.path:
        return 'web-app'
    LOG.info('Unable to extract resource type from path pattern (fallback to %s): %s' % (req.api, spec.path_pattern))
    return req.api


def extract_id_from_path(req):
    name = extract_name_from_path(req)
    pattern = req.spec_path_without_query()
    path = req.path_without_query()
    if name and (pattern and not pattern.endswith('}')) or (not pattern and not path.endswith('/%s' % name)):
        path = '%s/%s' % (path, name)
    return path


def extract_name_from_path(req):
    # verify if the path pattern ends with an ID param placeholder, otherwise bail
    if not re.match(r'.*/\{[^\}]+\}$', req.spec.path_pattern.split('?')[0]):
        return

    def is_id_param_name(param_name):
        return param_name in ['name', 'id'] or re.match(r'.+(Id|Name)', param_name or '')

    path_params = req.get_path_params()
    last_param = None
    last_param_idx = -1
    id_params = {k: v for k, v in path_params.items() if is_id_param_name(k)}
    for k, v in id_params.items():
        index = req.spec.path_pattern.index('{%s}' % k)
        if not last_param or index > last_param_idx:
            last_param = k
            last_param_idx = index
    if not last_param:
        return None
    return path_params[last_param]


def is_crud_operation(method_details):
    # TODO
    return True


def lookup_resource(resource_type, id_suffix=None, id_prefix=None):
    def matches(key):
        key = key.lower()
        if id_suffix and not key.endswith(id_suffix):
            return False
        if id_prefix and not key.startswith(id_prefix):
            return False
        return True
    id_suffix = id_suffix and id_suffix.lower()
    id_prefix = id_prefix and id_prefix.lower()
    map = _resource_map(resource_type)
    matching = [v for k, v in map.items() if matches(k)]
    params_str = []
    if id_prefix:
        params_str += ['prefix=%s' % id_prefix]
    if id_suffix:
        params_str += ['suffix=%s' % id_suffix]
    params_str = ', '.join(params_str)
    if not matching:
        LOG.debug('Unable to find %s resources for ID %s: %s' % (resource_type, params_str, list(map.keys())))
        return
    if len(matching) > 1:
        LOG.info('Found multiple %s resources for ID %s: %s' % (resource_type, params_str, matching))
    return matching[0]


def _resource_map(resource_type):
    # make sure to use a CaseInsensitiveDict for the ID matching below
    map = RESOURCES[resource_type] = RESOURCES.get(resource_type, CaseInsensitiveDict())
    return map
