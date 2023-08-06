import re
import json
import hashlib
import logging
from io import BytesIO
from requests.models import Request
from localstack.constants import TEST_AWS_ACCOUNT_ID
from localstack.utils.aws import aws_stack
from localstack.utils.common import to_str, to_bytes, short_uid, retry, FuncThread
from localstack.utils.analytics import event_publisher
from localstack.services.generic_proxy import ProxyListener
from localstack.utils.aws.aws_responses import requests_response

LOG = logging.getLogger(__name__)

EVENT_TYPE_CREATE_VAULT = 'glc.cv'
EVENT_TYPE_CREATE_JOB = 'glc.cj'

HEADER_ARCHIVE_ID = 'x-amz-archive-id'
HEADER_JOB_ID = 'x-amz-job-id'
HEADER_JOB_OUTPUT = 'x-amz-job-output-path'

PATH_PATTERN_BASE = '/([^/]+)/vaults/([^/]+)'
PATH_PATTERN_VAULTS = '^%s$' % PATH_PATTERN_BASE
PATH_PATTERN_JOBS = '^%s/jobs$' % PATH_PATTERN_BASE
PATH_PATTERN_ARCHIVES = '^%s/archives$' % PATH_PATTERN_BASE

# name pattern for S3 buckets used as storage backend for Glacier vaults
VAULT_BUCKET_NAME_PATTERN = 'glacier-vaults-{account}-{vault_name}'


class ProxyListenerGlacier(ProxyListener):

    def forward_request(self, method, path, data, headers):
        if method == 'OPTIONS':
            return 200

        # print('REQ', method, path, data)

        result = True
        if method == 'POST':
            if re.match(PATH_PATTERN_JOBS, path):
                data_dict = json.loads(to_str(data or '{}'))
                result = create_job(path, data_dict)
        elif method == 'PUT':
            if re.match(PATH_PATTERN_VAULTS, path):
                data_dict = json.loads(to_str(data or '{}'))
                result = create_vault(path, data_dict)

        if path.startswith('/-/') and result is True:
            modified_path = '/%s%s' % (TEST_AWS_ACCOUNT_ID, path[2:])
            return Request(data=data, url=modified_path, method=method, headers=headers)

        return result

    def return_response(self, method, path, data, headers, response):
        # print('!RESP', method, path, data, headers, response.status_code, response.content)
        if method == 'POST':
            if re.match(PATH_PATTERN_ARCHIVES, path):
                upload_archive(path, data, response)
            elif re.match(PATH_PATTERN_JOBS, path):
                data_dict = json.loads(to_str(data or '{}'))
                create_job(path, data_dict, response)


# ------------
# API METHODS
# ------------

def create_job(path, data, response=None):
    job_type = data.get('Type')
    account, vault_name = _extract_account_and_vault(path)
    result = True

    event_publisher.fire_event(EVENT_TYPE_CREATE_JOB, {'v': event_publisher.get_hash(vault_name)})

    if response is None:
        # request flow
        if job_type == 'select':
            result = create_job_select(account, vault_name, data)
    else:
        # response flow
        if job_type == 'archive-retrieval':
            result = create_job_archive(account, vault_name, data)
        elif job_type == 'inventory-retrieval':
            result = create_job_inventory(account, vault_name, data)

    sns_topic = data.get('SNSTopic')
    if sns_topic and response is not None:
        # wait for job completion, then send notification to SNS
        sns = aws_stack.connect_to_service('sns')
        glacier = aws_stack.connect_to_service('glacier')
        message = json.dumps(data)
        job_id = response.headers.get(HEADER_JOB_ID)

        def loop_check_job_done(*args):
            def check_job_done(*args):
                response = glacier.get_job_output(vaultName=vault_name, jobId=job_id)
                assert 'body' in response

            retry(check_job_done, sleep=2, retries=10)
            sns.publish(TopicArn=sns_topic, Message=message)

        # run loop in the background
        FuncThread(loop_check_job_done).start()

    return result


def create_job_select(account, vault_name, data):
    bucket_name = _vault_bucket_name(account, vault_name)
    params = data.get('SelectParameters')
    archive_id = data.get('ArchiveId')
    s3 = aws_stack.connect_to_service('s3')
    job_id = short_uid()
    job_key = _get_job_key(vault_name, job_id, account=account)

    # receive query results
    input_serial = params.get('InputSerialization') or {}
    output_serial = params.get('OutputSerialization') or {}
    if 'csv' in input_serial:
        input_serial['CSV'] = input_serial.pop('csv')
    if 'csv' in output_serial:
        output_serial['CSV'] = output_serial.pop('csv')
    archive_key = _get_archive_key(vault_name, archive_id, account=account)
    response = s3.select_object_content(
        Bucket=bucket_name, Key=archive_key, Expression=params.get('Expression'),
        ExpressionType=params.get('ExpressionType') or 'SQL',
        InputSerialization=input_serial, OutputSerialization=output_serial
    )

    # prepare output bucket

    output_path = '%s/results' % job_key
    output_bucket = bucket_name
    # get output path from request
    out_loc = data.get('OutputLocation', {}).get('S3')
    if out_loc:
        output_bucket = out_loc.get('BucketName')
        output_prefix = out_loc.get('Prefix')
        output_path = '%s/%s' % (output_prefix, job_id)

    # store results to destination bucket
    result_files = []
    for event in response['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload']
            result_key = '%s/results/%s' % (output_path, short_uid())
            result_files += ['s3://%s/%s' % (output_bucket, result_key)]
            LOG.debug('Uploading Glacier query results to bucket "%s"' % output_bucket)
            s3.upload_fileobj(BytesIO(records), output_bucket, result_key)

    data['JobId'] = job_id
    s3.upload_fileobj(BytesIO(to_bytes(json.dumps(data))), output_bucket, '%s/job.txt' % output_path)
    manifest_key = '%s/result_manifest.txt' % output_path
    s3.upload_fileobj(BytesIO(to_bytes('\n'.join(result_files))), output_bucket, manifest_key)

    headers = {
        'location': job_key,
        HEADER_JOB_ID: job_id,
        HEADER_JOB_OUTPUT: output_path
    }
    return requests_response('', headers=headers)


# TODO needed?
def create_job_archive(account, vault_name, data):
    result = True
    return result


# TODO needed?
def create_job_inventory(account, vault_name, data):
    result = True
    return result


def create_vault(path, data):
    account, vault_name = _extract_account_and_vault(path)

    event_publisher.fire_event(EVENT_TYPE_CREATE_VAULT, {'n': event_publisher.get_hash(vault_name)})

    bucket_name = _vault_bucket_name(account, vault_name)
    s3 = aws_stack.connect_to_service('s3')
    LOG.debug('Creating backend S3 bucket "%s" for Glacier vault "%s"' % (bucket_name, vault_name))
    s3.create_bucket(Bucket=bucket_name)
    return True


def upload_archive(path, data, response):
    account, vault_name = _extract_account_and_vault(path)
    bucket_name = _vault_bucket_name(account, vault_name)
    archive_id = response.headers.get(HEADER_ARCHIVE_ID)
    s3 = aws_stack.connect_to_service('s3')

    key = _get_archive_key(vault_name, archive_id, account=account)
    s3.upload_fileobj(BytesIO(data), bucket_name, key)

    hash_header = 'x-amz-sha256-tree-hash'
    if not response.headers.get(hash_header):
        response.headers[hash_header] = hashlib.sha256(data).hexdigest()
    if not response.headers.get('location'):
        response.headers['location'] = key


def _vault_bucket_name(account, vault_name):
    result = VAULT_BUCKET_NAME_PATTERN.format(account=account, vault_name=vault_name)
    # From AWS docs: allowed characters for vault name (max length 255): a-z, A-Z, 0-9, '_', '-', and '.'
    result = result.replace('_', '-').replace('.', '-')
    return result


def _extract_account_and_vault(path):
    pattern = '%s.*' % PATH_PATTERN_BASE
    account_id = re.sub(pattern, r'\1', path)
    account_id = TEST_AWS_ACCOUNT_ID if account_id == '-' else account_id
    return account_id, re.sub(pattern, r'\2', path)


def _get_archive_key(vault_name, archive_id, account=None):
    account = account or TEST_AWS_ACCOUNT_ID
    return '/%s/vaults/%s/archives/%s' % (account, vault_name, archive_id)


def _get_job_key(vault_name, job_id, account=None):
    account = account or TEST_AWS_ACCOUNT_ID
    return '/%s/vaults/%s/jobs/%s' % (account, vault_name, job_id)


# instantiate listener
UPDATE_GLACIER = ProxyListenerGlacier()
