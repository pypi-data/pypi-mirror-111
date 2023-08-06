import os
import re
import sys
import time
import logging
import traceback
import contextlib
import subprocess
from localstack import constants, config as localstack_config
from localstack.utils import bootstrap
from localstack.services import infra
from localstack.services import edge as localstack_edge
from localstack.utils.common import get_free_tcp_port, TMP_THREADS, ShellCommandThread, sleep_forever, to_str
from localstack.services.edge import ProxyListenerEdge as proxy
from localstack.utils.aws.aws_responses import requests_error_response, requests_error_response_json
from localstack_ext.services.xray.xray_listener import XRAY_API_PATHS
from localstack_ext.services.iam.policy_enforcer import enforce_iam_policies_for_request, CACHED_POLICIES

LOG = logging.getLogger(__name__)

# IoT path prefixes, used for edge routing
IOT_PATH_PREFIXES = [
    '/tags', '/things', '/thing-groups', '/wireless-devices', '/indices', '/rules', '/dimensions',
    '/policies', '/certificates', '/jobs', '/target-policies', '/authorizer', '/billing-groups',
    '/domainConfigurations', '/role-aliases', '/streams', '/thing-types', '/dynamic-thing-groups'
]

# maps account_ID -> service_name -> service_port
ACCOUNTS_TO_SERVICE_PORTS = {}

# API shared locks
API_LOCKS = {}

# generic global state dict
STATE = {}


def current_timestamp():
    return int(round(time.time() * 1000))


def start_multi_account_router(parts, asynchronous):
    api_names = bootstrap.canonicalize_api_names()
    cmd = '%s %s start --host' % (sys.executable,
        os.path.join(constants.LOCALSTACK_ROOT_FOLDER, 'localstack', 'utils', 'cli.py'))

    reserved_ports = []

    # start separate instance for each configured account
    for account_id in parts:
        ACCOUNTS_TO_SERVICE_PORTS[account_id] = port_mappings = {}
        services = ''

        # configure API ports
        for api in api_names:
            port = get_free_tcp_port(blacklist=reserved_ports)
            reserved_ports.append(port)
            port_mappings[api] = port
            services += '%s%s:%s' % (',' if services else '', api, port)

        # configure edge_port
        edge_port = get_free_tcp_port(blacklist=reserved_ports)
        reserved_ports.append(edge_port)
        port_mappings['edge'] = edge_port

        LOG.debug('Using random service ports for account ID %s: %s' % (account_id, services))
        env_vars = {
            'SERVICES': services,
            'EDGE_PORT': str(edge_port),
            'TEST_AWS_ACCOUNT_ID': account_id,
            'DNS_ADDRESS': '0',
            'PYTHONPATH': '.:%s' % constants.LOCALSTACK_ROOT_FOLDER
        }
        thread = ShellCommandThread(cmd, outfile=subprocess.PIPE, env_vars=env_vars)
        TMP_THREADS.append(thread)
        thread.start()

    # start edge service
    localstack_edge.start_edge(asynchronous=True)

    if not asynchronous:
        sleep_forever()


def patch_start_edge():
    from localstack_ext.services.cognito import cognito_listener
    from localstack_ext.services.apigateway.apigateway_extended import is_custom_domain_api_invocation

    def do_start_infra(asynchronous, *args, **kwargs):
        parts = re.split(r'[\s,;]+', constants.TEST_AWS_ACCOUNT_ID.strip())
        parts = set(parts)
        if len(parts) > 1:
            return start_multi_account_router(parts, asynchronous)
        return do_start_infra_orig(asynchronous, *args, **kwargs)

    do_start_infra_orig = infra.do_start_infra
    infra.do_start_infra = do_start_infra

    def get_service_port_for_account(service, headers, *args, **kwargs):
        auth_header = headers.get('authorization', '')
        credential = auth_header.split('Credential=')[-1]
        access_key = credential.split('/')[0]
        if ACCOUNTS_TO_SERVICE_PORTS:
            # TODO: in the future, we should maintain a mapping between access_key and account ID
            account_config = ACCOUNTS_TO_SERVICE_PORTS.get(access_key) or {}
            target_port = account_config.get('edge')
            if target_port:
                return target_port
            return -1
        return get_service_port_for_account_orig(service, headers, *args, **kwargs)

    get_service_port_for_account_orig = localstack_edge.get_service_port_for_account
    localstack_edge.get_service_port_for_account = get_service_port_for_account

    def get_api_from_headers(headers, method=None, path=None, data=None, **kwargs):

        auth_header = headers.get('authorization', '')
        host = headers.get('host', '')
        target = headers.get('x-amz-target', '')
        path = path or '/'
        path_without_params = path.split('?')[0]
        if '/elasticmapreduce/' in auth_header:
            return 'emr', localstack_config.PORT_EMR, path, host
        if cognito_listener.is_cognito_idp_request(path, headers):
            return 'cognito-idp', localstack_config.PORT_COGNITO_IDP, path, host
        if path.startswith('/_messages_'):
            return 'ses', localstack_config.PORT_SES, path, host
        if path == '/xray_records':
            return 'xray', localstack_config.PORT_XRAY, path, host
        if target.startswith('AmazonAthena.'):
            return 'athena', localstack_config.PORT_ATHENA, path, host
        if '.cloudfront.' in host:
            return 'cloudfront', localstack_config.PORT_CLOUDFRONT, path, host
        if '.elb.' in host:
            return 'elbv2', localstack_config.PORT_ELBV2, path, host
        # Note: IoT API is using 'execute-api' as signing name
        if '/execute-api/' in auth_header:
            if any(path.startswith(prefix) for prefix in IOT_PATH_PREFIXES) or path_without_params == '/endpoint':
                return 'iot', localstack_config.PORT_IOT, path, host
            if path_without_params.startswith('/@connections/'):
                return 'apigateway', localstack_config.PORT_APIGATEWAY, path, host
        if re.match(r'/graphql/[a-zA-Z0-9-]+', path):
            return 'appsync', localstack_config.PORT_APPSYNC, path, host
        if '/elasticloadbalancing/' in auth_header:
            data_str = to_str(data or '')
            if any('Version=2015-12-01' in s for s in [path, data_str]):
                return 'elbv2', localstack_config.PORT_ELBV2, path, host
            if any('Version=2012-06-01' in s for s in [path, data_str]):
                return 'elb', localstack_config.PORT_ELB, path, host
        if '/2018-06-01/runtime' in path:
            return 'lambda', localstack_config.PORT_LAMBDA, path, host
        if method == 'POST' and path in XRAY_API_PATHS:
            return 'xray', localstack_config.PORT_XRAY, path, host
        if auth_header.startswith('Bearer '):
            return 'apigateway', localstack_config.PORT_APIGATEWAY, path, host

        # call the original method to see if we have a match with the base logic
        result = get_api_from_headers_orig(headers, path=path, data=None, **kwargs)

        if result:
            result = list(result)
            if result[0] == 'iotdata':
                result[0] = 'iot-data'
            if result[0] == 'iotanalytics':
                result[0] = 'iot-analytics'
            if result[0] == 'iotwireless':
                result[0] = 'iot'
            if result[0] != localstack_edge.API_UNKNOWN:
                return result

        if not result or result[0] == localstack_edge.API_UNKNOWN:
            # fall back - check if this is an API Gateway custom domain invocation
            if is_custom_domain_api_invocation(method=method, path=path, data=data, headers=headers):
                return 'apigateway', localstack_config.PORT_APIGATEWAY, path, host
        return result

    get_api_from_headers_orig = localstack_edge.get_api_from_headers
    localstack_edge.get_api_from_headers = get_api_from_headers

    def get_lock_for_request(api, method, path, data, headers, *args, **kwargs):
        persistence_details = API_LOCKS.get(api, {})
        lock = None
        if persistence_details:
            rwlock = persistence_details.get('rwlock')
            get_lock_func = persistence_details.get('get_lock_func')
            if get_lock_func:
                lock = get_lock_func(rwlock, method, path, data, headers, *args, **kwargs)
            else:
                lock = rwlock.gen_rlock()
        lock = lock or contextlib.nullcontext()
        return lock

    def return_response(self, method, path, data, headers, *args, **kwargs):
        api = get_api_from_headers(headers, method=method, path=path, data=data)[0]

        persistence_details = API_LOCKS.get(api, {})
        lock = contextlib.nullcontext()
        if persistence_details:
            rwlock = persistence_details.get('rwlock')
            update_funcs = persistence_details.get('update_func') or persistence_details.get('update_funcs')
            update_funcs = update_funcs if isinstance(update_funcs, list) else [update_funcs]
            for update_func in update_funcs:
                update_func(rwlock, method, path, data=data, headers=headers)
            lock = get_lock_for_request(api, method, path, data, headers, *args, **kwargs)

        with lock:
            return return_response_orig(self, method, path, data, headers, *args, **kwargs)

    return_response_orig = proxy.return_response
    proxy.return_response = return_response

    def do_forward_request(api, method, path, data, headers, *args, **kwargs):
        # print('!EDGE', method, path, len(data or ''), headers.get('Authorization'))
        try:
            if api == 'iam':
                # clear policy cache in case of IAM requests
                CACHED_POLICIES.clear()
            # enforce IAM policies
            enforce_iam_policies_for_request(api, method, path, data, headers)
        except Exception as e:
            kwargs = {
                'message': 'Access to the specified resource is denied',
                'code': 403, 'error_type': 'AccessDeniedException'
            }
            if api in ['lambda']:
                response = requests_error_response_json(**kwargs)
            else:
                response = requests_error_response(headers, **kwargs)
            # print traceback only for non-well known errors
            t = '' if 'denied' in str(e) or 'found' in str(e) else traceback.format_exc()
            LOG.debug('Denying request for API "%s" due to IAM enforcement: %s %s - %s %s' % (api, method, path, e, t))
            return response

        return do_forward_request_orig(api, method, path, data, headers, *args, **kwargs)

    do_forward_request_orig = localstack_edge.do_forward_request
    localstack_edge.do_forward_request = do_forward_request

    # Apply fix to create "real" daemon threads (see https://stackoverflow.com/a/62731225/11534915)
    # TODO: fix upstream
    from localstack.utils.async_utils import THREAD_POOL
    import concurrent.futures

    def _submit(self, *args, **kwargs):
        result = _submit_orig(self, *args, **kwargs)
        if not STATE.get('_queue_removed_'):
            STATE['_queue_removed_'] = True
            try:
                del concurrent.futures.thread._threads_queues[list(THREAD_POOL._threads)[0]]
            except Exception:
                # fail silently if this functionality is not available
                pass
        return result
    _submit_orig = THREAD_POOL.submit
    THREAD_POOL.submit = _submit

    patch_case_sensitive_headers()


def patch_case_sensitive_headers():
    """ Apply patches to enable case-sensitive HTTP headers. This is required to enable
        certain AWS SDK clients (e.g., AWS S3 client for Apache Flink/Beam). """
    from quart import asgi, utils as quart_utils
    from hypercorn import utils
    from hypercorn.protocol import http_stream

    # patch _encode_headers(..) to return case-sensitive headers

    def _encode_headers(headers):
        return [(key.encode(), value.encode()) for key, value in headers.items()]

    asgi._encode_headers = asgi.encode_headers = quart_utils.encode_headers = _encode_headers

    # patch build_and_validate_headers(..) to pass case-sensitive headers from `headers_original`

    def build_and_validate_headers(headers):
        validated_headers = []
        for name, value in headers:
            if name[0] == b':'[0]:
                raise ValueError('Pseudo headers are not valid')
            validated_headers.append((bytes(name).strip(), bytes(value).strip()))
        return validated_headers

    utils.build_and_validate_headers = http_stream.build_and_validate_headers = build_and_validate_headers
