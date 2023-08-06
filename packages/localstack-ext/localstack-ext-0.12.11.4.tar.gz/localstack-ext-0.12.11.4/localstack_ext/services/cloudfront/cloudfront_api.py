import re
import logging
import xmltodict
from flask import Flask, request, make_response
from six.moves.urllib import parse as urlparse
from requests.structures import CaseInsensitiveDict
from localstack.constants import LOCALHOST, HEADER_LOCALSTACK_EDGE_URL
from localstack.utils.common import (
    to_str, short_uid, clone, epoch_timestamp, select_attributes, safe_requests as requests)
from localstack.utils.analytics import event_publisher
from localstack.services.generic_proxy import ProxyListener, serve_flask_app, start_proxy_server, RegionBackend
from localstack.utils.aws.aws_responses import (
    requests_to_flask_response, requests_response, flask_error_response_xml)
from localstack_ext import config as ext_config
from localstack_ext.utils.aws import aws_utils
from localstack_ext.utils.common import get_available_service_instance_port

LOG = logging.getLogger(__name__)

APP_NAME = 'cloudfront_api'
app = Flask(APP_NAME)

XMLNS_CLOUDFRONT = 'http://cloudfront.amazonaws.com/doc/2013-11-11/'

# API constants
BASE_PATH = '/<version>/'

# domain name and URL patterns
# DOMAIN_NAME_PATTERN = '%s.cloudfront.net'
DOMAIN_NAME_PATTERN = '%s.cloudfront.{}'.format(ext_config.LOCAL_HOSTNAME)
DISTRIBUTION_URL_PATTERN = r'https?://([^.]+)\.cloudfront.(net|localhost\.localstack\.cloud)(.*)'

# list of HTTP methods
ALL_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']

# event types
EVENT_TYPE_CREATE_DISTRIBUTION = 'cfr.cd'
EVENT_TYPE_DELETE_DISTRIBUTION = 'cfr.dd'


class CloudFrontState(RegionBackend):
    def __init__(self):
        # maps ID to distribution details
        self.distributions = {}
        # list of origin access identities
        self.origin_access_identities = []
        # maps name to function details
        self.functions = {}
        # maps policy ID to origin request policy details
        self.origin_request_policies = {}

    @classmethod
    def get_current_request_region(cls):
        # Note: no regions required - distributions are global
        return 'global'


class Distribution(object):
    def __init__(self, params=None):
        self.params = params
        self.invalidations = {}


class ProxyListenerCloudFront(ProxyListener):
    def __init__(self, distribution_id):
        self.distr_url = 'https://%s/' % (DOMAIN_NAME_PATTERN % distribution_id)

    def forward_request(self, method, path, data, headers):
        response = invoke_distribution(self.distr_url, method=method, path=path, data=data, headers=headers)
        return response


# ------------------
# API METHODS BELOW
# ------------------

# -------------------
# Distributions APIs
# -------------------

@app.route('%sdistribution' % BASE_PATH, methods=['GET'])
def list_distributions(version):
    def convert(d):
        result = clone(d['Distribution'])
        config = result.pop('DistributionConfig', {})
        config.get('Origins', {})['Items'] = {'Origin': config.get('Origins', {}).get('Items')}
        for k, v in config.items():
            result[k] = v
        return result

    state = CloudFrontState.get()
    distrs = [convert(d.params) for d in state.distributions.values()]
    result = {
        'DistributionList': {
            'Items': {
                'DistributionSummary': distrs
            },
            'Quantity': len(distrs)
        }
    }
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%sdistribution' % BASE_PATH, methods=['POST'])
def create_distribution(version):
    distr_entry = {}
    state = CloudFrontState.get()

    distr_id = short_uid()
    domain_name = DOMAIN_NAME_PATTERN % distr_id
    port = 0
    if ext_config.CLOUDFRONT_STATIC_PORTS:
        port = get_available_service_instance_port()
        distr_id = 'cf-%s' % port
        domain_name = 'localhost:%s' % port
        listener = ProxyListenerCloudFront(distr_id)
        thread = start_proxy_server(port, update_listener=listener, use_ssl=True)
        # TODO: stop listener once distribution gets deleted
        distr_entry['_thread_'] = thread

    event_publisher.fire_event(EVENT_TYPE_CREATE_DISTRIBUTION, {'q': event_publisher.get_hash(distr_id)})
    details = get_payload()
    with_tags = details.get('DistributionConfigWithTags', {})
    config = (with_tags or details)['DistributionConfig']

    def fix_keys(key, entry):
        items = (entry or {}).get('Items', {})
        if entry and isinstance(items, dict) and list(items.keys()) == [key]:
            items = items[key]
            entry['Items'] = items if isinstance(items, list) else [items]

    # fix some entries that may be incorrect due to xmltodict conversion
    for key in ['Origin', 'CacheBehavior']:
        fix_keys(key, config.get('%ss' % key))
    for entries in [config.get('CacheBehaviors', {}).get('Items', []), [config.get('DefaultCacheBehavior')]]:
        for entry in entries or []:
            fix_keys('Method', entry.get('AllowedMethods'))
            fix_keys('Method', entry.get('AllowedMethods', {}).get('CachedMethods'))

    tags = with_tags.get('Tags') or []
    distr_entry.update({
        'Distribution': {
            'Id': distr_id,
            'ARN': aws_utils.get_cloudfront_distribution_arn(distr_id),
            'DomainName': domain_name,
            'DistributionConfig': config,
            'Tags': tags
        }
    })
    state.distributions[distr_id] = Distribution(distr_entry)
    result = dict(distr_entry)
    result.pop('_thread_', None)
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%sdistribution/<distr_id>' % BASE_PATH, methods=['DELETE'])
def delete_distribution(version, distr_id):
    state = CloudFrontState.get()
    distr = state.distributions.pop(distr_id, None)
    if not distr:
        return not_found_error('Unable to find CloudFront distribution "%s"' % distr_id)
    return make_response('')


# -------------------
# Invalidations APIs
# -------------------

@app.route('%sdistribution/<distr_id>/invalidation' % BASE_PATH, methods=['POST'])
def create_invalidation(version, distr_id):
    state = CloudFrontState.get()
    distr = state.distributions.get(distr_id)
    if not distr:
        return not_found_error('Unable to find CloudFront distribution "%s"' % distr_id)
    details = get_payload()
    inval_id = short_uid()
    details['CreateTime'] = epoch_timestamp()
    details['Id'] = inval_id
    distr.invalidations[inval_id] = details
    result = {'Invalidation': details}
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%sdistribution/<distr_id>/invalidation' % BASE_PATH, methods=['GET'])
def list_invalidations(version, distr_id):
    state = CloudFrontState.get()
    distr = state.distributions.get(distr_id)
    if not distr:
        return not_found_error('Unable to find CloudFront distribution "%s"' % distr_id)
    result = list(distr.invalidations.values())
    summary_attrs = ['CreateTime', 'Id', 'Status']
    result = {
        'InvalidationList': {
            'Items': [{'InvalidationSummary': select_attributes(i, summary_attrs)} for i in result],
            'Quantity': len(result)
        }
    }
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%sdistribution/<distr_id>/invalidation/<inval_id>' % BASE_PATH, methods=['GET'])
def get_invalidation(version, distr_id, inval_id):
    state = CloudFrontState.get()
    distr = state.distributions.get(distr_id)
    if not distr:
        return not_found_error('Unable to find CloudFront distribution "%s"' % distr_id)
    result = distr.invalidations.get(inval_id)
    if not result:
        return not_found_error('Unable to find invalidation %s for distribution "%s"' % (inval_id, distr_id))
    result = {'Invalidation': result}
    result = xmltodict.unparse(result)
    return make_response(result)


# ---------------
# Functions APIs
# ---------------

@app.route('%s/function' % BASE_PATH, methods=['POST'])
def create_function(version):
    state = CloudFrontState.get()
    entry = get_payload().get('CreateFunctionRequest', {})
    entry['ETag'] = short_uid()
    if state.functions.get(entry['Name']):
        return error_response('CloudFront function "%s" already exists' % entry['Name'], code=400)
    state.functions[entry['Name']] = entry
    result = {'FunctionSummary': entry}
    result = xmltodict.unparse(result)
    headers = {'Location': 'TODO', 'ETag': entry['ETag']}
    return make_response(result), 200, headers


@app.route('%s/function' % BASE_PATH, methods=['GET'])
def list_functions(version):
    state = CloudFrontState.get()
    result = list(state.functions.values())
    result = {'FunctionsList': {
        'Items': {'FunctionSummary': result},
        'Quantity': len(result)
    }}
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%s/function/<func_name>' % BASE_PATH, methods=['GET'])
def get_function(version, func_name):
    state = CloudFrontState.get()
    function = state.functions.get(func_name)
    if not function:
        return error_response('Unable to find function named "%s"' % func_name,
            code=404, error_type='NoSuchFunctionExists')
    result = {'Function': function}
    result = xmltodict.unparse(result)
    headers = {'ETag': function['ETag']}
    return make_response(result), 200, headers


@app.route('%s/function/<func_name>' % BASE_PATH, methods=['PUT'])
def update_function(version, func_name):
    state = CloudFrontState.get()
    entry = state.functions.get(func_name)
    if not entry:
        return not_found_error('Unable to find CloudFront function "%s" for update' % func_name)
    data = get_payload()
    data = data.get('UpdateFunctionRequest', {})
    entry['FunctionConfig'].update(data['FunctionConfig'])
    entry['FunctionCode'] = data['FunctionCode']
    result = {'FunctionSummary': entry}
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%s/function/<func_name>' % BASE_PATH, methods=['DELETE'])
def delete_function(version, func_name):
    state = CloudFrontState.get()
    entry = state.functions.pop(func_name, None)
    if not entry:
        return not_found_error('Unable to find CloudFront function "%s" for deletion' % func_name)
    return ''


# ---------------------------
# Origin Request Policy APIs
# ---------------------------

@app.route('%s/origin-request-policy' % BASE_PATH, methods=['POST'])
def create_origin_request_policy(version):
    state = CloudFrontState.get()
    entry = get_payload()
    entry['Id'] = short_uid()
    entry['ETag'] = short_uid()
    policy_name = entry['OriginRequestPolicyConfig']['Name']
    existing = [p for p in state.origin_request_policies.values() if
        p['OriginRequestPolicyConfig']['Name'] == policy_name]
    if existing:
        return error_response('CloudFront origin request policy "%s" already exists' % policy_name, code=400)
    state.origin_request_policies[entry['Id']] = entry
    result = {'OriginRequestPolicy': entry}
    result = xmltodict.unparse(result)
    headers = {'Location': 'TODO', 'ETag': entry['ETag']}
    return make_response(result), 200, headers


@app.route('%s/origin-request-policy' % BASE_PATH, methods=['GET'])
def list_origin_request_policies(version):
    state = CloudFrontState.get()
    result = list(state.origin_request_policies.values())
    items = [{'Id': r.get('Id'), 'OriginRequestPolicy': r} for r in result]
    result = {'OriginRequestPolicyList': {
        'Items': {'OriginRequestPolicySummary': items}, 'Quantity': len(result)
    }}
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%s/origin-request-policy/<policy_id>' % BASE_PATH, methods=['GET'])
def get_origin_request_policy(version, policy_id):
    state = CloudFrontState.get()
    policy = state.origin_request_policies.get(policy_id)
    if not policy:
        return error_response('Unable to find origin request policy ID "%s"' % policy_id,
            code=404, error_type='NoSuchOriginRequestPolicy')
    result = {'OriginRequestPolicy': policy}
    result = xmltodict.unparse(result)
    headers = {'ETag': policy['ETag']}
    return make_response(result), 200, headers


@app.route('%s/origin-request-policy/<policy_id>' % BASE_PATH, methods=['PUT'])
def update_origin_request_policy(version, policy_id):
    state = CloudFrontState.get()
    data = get_payload()
    entry = state.origin_request_policies.get(policy_id)
    if not entry:
        return not_found_error('Unable to find CloudFront origin request policy "%s" for update' % policy_id)
    entry['OriginRequestPolicyConfig'].update(data['OriginRequestPolicyConfig'])
    result = {'OriginRequestPolicy': entry}
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%s/origin-request-policy/<policy_id>' % BASE_PATH, methods=['DELETE'])
def delete_origin_request_policy(version, policy_id):
    state = CloudFrontState.get()
    entry = state.origin_request_policies.pop(policy_id, None)
    if not entry:
        return not_found_error('Unable to find CloudFront origin request policy "%s" for deletion' % policy_id)
    return ''


# ----------------------------
# Origin Access Identity APIs
# ----------------------------

@app.route('%s/origin-access-identity/cloudfront' % BASE_PATH, methods=['GET'])
def list_origin_access_identities(version):
    state = CloudFrontState.get()
    result = state.origin_access_identities
    result = [{'Comment': r.get('CloudFrontOriginAccessIdentityConfig', {}).get('Comment'), **r} for r in result]
    result = {'Items': {'CloudFrontOriginAccessIdentitySummary': result}, 'Quantity': len(result)}
    result = {'CloudFrontOriginAccessIdentityList': result}
    result = xmltodict.unparse(result)
    return make_response(result)


@app.route('%s/origin-access-identity/cloudfront' % BASE_PATH, methods=['POST'])
def create_origin_access_identities(version):
    state = CloudFrontState.get()
    entry = get_payload()
    entry['Id'] = short_uid()
    entry['S3CanonicalUserId'] = 's3-cf-user'  # TODO
    state.origin_access_identities.append(entry)
    result = {'CloudFrontOriginAccessIdentity': entry}
    result = xmltodict.unparse(result)
    headers = {'Location': 'TODO', 'ETag': short_uid()}
    return make_response(result), 200, headers


# ---------------
# Fallback route
# ---------------

@app.route('/', defaults={'path': ''}, methods=ALL_METHODS)
@app.route('/<path:path>', methods=ALL_METHODS)
def fallback(path):
    edge_url = request.headers.get(HEADER_LOCALSTACK_EDGE_URL, '')
    if re.match(DISTRIBUTION_URL_PATTERN, edge_url):
        path_with_params = '%s?%s' % (path, to_str(request.query_string))
        response = invoke_distribution(edge_url, request.method,
            path='/%s' % path_with_params, data=request.data, headers=request.headers)
        return requests_to_flask_response(response)
    msg = 'Not yet implemented: Unable to find path mapping for %s /%s' % (request.method, path)
    LOG.warning(msg)
    return make_response(msg), 404


# ---------------
# HELPER METHODS
# ---------------

def is_aws_domain(domain):
    return re.match(r'.*((aws\.amazon)|amazonaws)\.com', domain or '')


def invoke_distribution(edge_url, method, path, data, headers):
    match = re.match(DISTRIBUTION_URL_PATTERN, edge_url)
    distr_id = match.group(1)
    headers = CaseInsensitiveDict(headers)
    path_without_params = urlparse.urlparse(path).path
    origin = get_matching_origin(distr_id, method, path_without_params)
    if not origin:
        return requests_response('', status_code=404)

    domain = origin.get('DomainName')
    target_host = LOCALHOST if is_aws_domain(domain) else domain
    target_path = '%s%s' % (origin.get('OriginPath') or '', path)
    target_path = target_path.replace('//', '/')
    headers['Host'] = domain
    url = 'https://%s%s' % (target_host, target_path)
    LOG.info('Forwarding CloudFront invocation to URL %s, Host header "%s"' % (url, domain))

    function = getattr(requests, method.lower())
    response = function(url, data=data, headers=headers, verify=False)
    return response


def get_matching_origin(distr_id, method, path):
    state = CloudFrontState.get()
    distr = state.distributions.get(distr_id)
    if not distr:
        return
    distr = distr.params
    config = distr['Distribution']['DistributionConfig']
    caches = config.get('CacheBehaviors', {}).get('Items', [])

    matching_origin = None
    for cache in caches:
        pattern = cache.get('PathPattern', '').replace('*', '.*')
        if re.match(pattern, path):
            if method in cache.get('AllowedMethods', {}).get('Items', []):
                matching_origin = cache.get('TargetOriginId')
                break

    if not matching_origin:
        default_cache = config.get('DefaultCacheBehavior')
        matching_origin = default_cache.get('TargetOriginId')

    origins = config.get('Origins', {}).get('Items', [])
    origin = ([o for o in origins if o.get('Id') == matching_origin] or [0])[0]
    return origin


def get_payload():
    return clone(xmltodict.parse(to_str(request.data)))


def error_response(msg, code=400, error_type='Exception'):
    LOG.warning(msg)
    return flask_error_response_xml(msg, code, error_type, xmlns=XMLNS_CLOUDFRONT)


def not_found_error(msg, error_type='ResourceNotFoundError'):
    return error_response(msg, code=404, error_type=error_type)


def serve(port, quiet=True):
    return serve_flask_app(app=app, port=port, quiet=quiet)
