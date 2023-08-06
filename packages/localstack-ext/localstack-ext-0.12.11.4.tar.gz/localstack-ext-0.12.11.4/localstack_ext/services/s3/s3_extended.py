import os
import types
import logging
import xmltodict
from localstack_ext import config
from readerwriterlock import rwlock
from moto.s3.responses import s3_backend
from localstack import config as localstack_config
from localstack.utils.aws import aws_stack
from localstack.services.s3 import s3_listener, s3_utils
from localstack.utils.common import new_tmp_file, rm_rf, json_safe
from localstack.utils.aws.aws_responses import requests_response
from localstack_ext.services.s3.s3_select_utils import (
    query_csv, query_json, convert_to_s3_select_payload, format_s3_select_result
)
from localstack_ext.services.edge import API_LOCKS
from localstack_ext.utils.persistence import load_backend_state, persist_state

LOG = logging.getLogger(__name__)

S3_STATES_DIR = os.path.join(config.BACKEND_STATES_DIR, 's3')


def run_query(bucket, key, query, input_serialization):
    s3 = aws_stack.connect_to_service('s3')
    tmp_file = new_tmp_file()
    s3.download_file(bucket, key, tmp_file)
    formats = [k.lower() for k in input_serialization.keys()]

    if 'json' in formats:
        result = query_json(query, tmp_file, input_serialization=input_serialization)
    elif 'csv' in formats:
        result = query_csv(query, tmp_file, input_serialization=input_serialization)

    rm_rf(tmp_file)
    return result


def update_backend_state(lock, method, path, *args, **kwargs):
    if not localstack_config.DATA_DIR:
        return
    if method != 'PUT':
        return

    bucket_name = path[1:].split('/')[0]
    state = s3_backend.buckets.get(bucket_name)

    if state:
        # S3 is global service, we don't need to specify region
        persist_state(S3_STATES_DIR, '_', bucket_name, state, lock)


def load_persistence_state():
    if not localstack_config.DATA_DIR:
        return
    for key, _, bucket in load_backend_state(S3_STATES_DIR):
        s3_backend.buckets[key] = bucket


def get_lock_for_request(rwlock, method, *args, **kwargs):
    if method in ['POST', 'PUT']:
        return rwlock.gen_wlock()
    return rwlock.gen_rlock()


def patch_s3():
    # patch existing listener methods
    def forward_request(self, method, path, data, headers):
        if method == 'POST' and '?select' in path or '&select' in path:
            body = xmltodict.parse(data)
            body = body.get('SelectObjectContentRequest')
            if body:
                expr_type = body.get('ExpressionType')
                if expr_type != 'SQL':
                    LOG.warning('Unexpected S3 Select expression type: %s' % expr_type)
                else:
                    output_serialization = body.get('OutputSerialization')
                    input_serialization = body.get('InputSerialization')
                    expr = body.get('Expression')
                    bucket, key = s3_utils.extract_bucket_and_key_name(headers, path)
                    result = run_query(bucket, key, expr, input_serialization=input_serialization)
                    result = json_safe(result)
                    result = format_s3_select_result(result, output_serialization)
                    payload_raw = convert_to_s3_select_payload(result)
                    return requests_response(payload_raw)

        result = forward_request_orig(method, path, data, headers)
        return result

    forward_request_orig = s3_listener.UPDATE_S3.forward_request
    s3_listener.UPDATE_S3.forward_request = types.MethodType(forward_request, s3_listener.UPDATE_S3)

    if 's3' not in API_LOCKS:
        lock = rwlock.RWLockRead()
        API_LOCKS['s3'] = {
            'rwlock': lock,
            'update_func': update_backend_state,
            'get_lock_func': get_lock_for_request
        }

    load_persistence_state()
