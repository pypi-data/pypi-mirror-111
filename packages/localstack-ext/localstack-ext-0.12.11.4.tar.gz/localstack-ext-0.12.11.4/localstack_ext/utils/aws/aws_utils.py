import re
import logging
import threading
from flask import request
from requests.models import Request
from requests.structures import CaseInsensitiveDict
from localstack.constants import INTERNAL_AWS_ACCESS_KEY_ID
from localstack.services import generic_proxy
from localstack.utils.aws import aws_stack
from localstack.utils.common import to_str
from localstack.utils.bootstrap import FuncThread

LOG = logging.getLogger(__name__)

get_region_orig = aws_stack.get_region
modify_and_forward_orig = generic_proxy.modify_and_forward

THREAD_LOCAL = threading.local()

MARKER_APIGW_REQUEST_REGION = '__apigw_request_region__'


def modify_and_forward(method=None, path=None, data_bytes=None, headers=None, *args, **kwargs):
    """ Patch proxy forward method and store request in thread local. """
    request_context = None
    if not getattr(THREAD_LOCAL, 'request_context', None):
        request_context = Request(url=path, data=data_bytes, headers=headers, method=method)
    with RequestContextManager(request_context):
        result = modify_and_forward_orig(method, path, data_bytes=data_bytes, headers=headers, *args, **kwargs)
    return result


def get_proxy_request_for_thread():
    try:
        return THREAD_LOCAL.request_context
    except Exception:
        return None


def get_flask_request_for_thread():
    try:
        return Request(url=request.path, data=request.data,
            headers=CaseInsensitiveDict(request.headers), method=request.method)
    except Exception as e:
        # swallow error: "Working outside of request context."
        if 'Working outside' in str(e):
            return None
        raise


def extract_region_from_auth_header(headers):
    # TODO: use method from aws_stack, which currently causes stack overflow due to call to get_region()!
    auth = headers.get('Authorization') or ''
    region = re.sub(r'.*Credential=[^/]+/[^/]+/([^/]+)/.*', r'\1', auth)
    if region == auth:
        return None
    region = region or aws_stack.get_local_region()
    return region


def get_request_context():
    candidates = [get_proxy_request_for_thread(), get_flask_request_for_thread()]
    for req in candidates:
        if req is not None:
            return req


def set_default_region_in_request_context(service, region):
    request_context = get_request_context()
    if not request_context:
        LOG.info('Unable to find context for request to service "%s" in region "%s": %s' %
            (service, region, request_context))
        return
    aws_stack.set_default_region_in_headers(request_context.headers, service=service, region=region)


def get_region(*args, **kwargs):
    request_context = get_request_context()
    if request_context:
        region = extract_region_from_auth_header(request_context.headers)
        # TODO: fix region lookup for other requests, e.g., API gateway invocations
        # that do not contain region details in the Authorization header.
        region = region or request_context.headers.get(MARKER_APIGW_REQUEST_REGION)
        if region:
            return region
    return get_region_orig(*args, **kwargs)


def set_default_region_in_headers(headers, *args, **kwargs):
    # This should be a no-op in Pro, as we support arbitrary regions and don't use a "default" region
    pass


class RequestContextManager(object):
    """ Context manager which sets the given request context (i.e., region) for the scope of the block. """

    def __init__(self, request_context):
        self.request_context = request_context

    def __enter__(self):
        THREAD_LOCAL.request_context = self.request_context

    def __exit__(self, type, value, traceback):
        THREAD_LOCAL.request_context = None


def is_internal_call_context():
    """ Return whether we are executing in the context of an internal API call, i.e.,
        the case where one API uses a boto3 client to call another API internally. """
    request_context = get_request_context()
    if request_context:
        auth_header = request_context.headers.get('Authorization') or ''
        header_value = 'Credential=%s/' % INTERNAL_AWS_ACCESS_KEY_ID
        return header_value in auth_header


def patch_aws_stack():
    aws_stack.get_region = get_region
    generic_proxy.modify_and_forward = modify_and_forward
    aws_stack.set_default_region_in_headers = set_default_region_in_headers

    # make sure that we inherit THREAD_LOCAL request contexts to spawned sub-threads

    def thread_init(self, *args, **kwargs):
        self._req_context = get_request_context()
        return thread_init_orig(self, *args, **kwargs)

    def thread_run(self, *args, **kwargs):
        if self._req_context:
            THREAD_LOCAL.request_context = self._req_context
        return thread_run_orig(self, *args, **kwargs)

    thread_run_orig = FuncThread.run
    FuncThread.run = thread_run
    thread_init_orig = FuncThread.__init__
    FuncThread.__init__ = thread_init


def download_s3_object(bucket_or_url, key=None, as_str=False):
    s3_client = aws_stack.connect_to_service('s3')
    bucket = bucket_or_url
    if bucket_or_url.startswith('s3://'):
        bucket, _, key = bucket_or_url[len('s3://'):].partition('/')
    downloaded_object = s3_client.get_object(Bucket=bucket, Key=key)
    downloaded_content = downloaded_object['Body'].read()
    if as_str:
        downloaded_content = to_str(downloaded_content)
    return downloaded_content


# -------------------
# ARN UTIL FUNCTIONS
# -------------------

def get_events_rule_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:events:%s:%s:rule/%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def get_eks_cluster_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:eks:%s:%s:cluster/%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def get_cloudfront_distribution_arn(id, account_id=None, region_name=None):
    account_id = aws_stack.get_account_id(account_id)
    return 'arn:aws:cloudfront::%s:distribution/%s' % (account_id, id)


def get_cloudfront_function_arn(name, account_id=None, region_name=None):
    account_id = aws_stack.get_account_id(account_id)
    return 'arn:aws:cloudfront::%s:function/%s' % (account_id, name)


def get_userpool_arn(pool_id, account_id=None, region_name=None):
    pattern = 'arn:aws:cognito-idp:%s:%s:userpool/%s'
    return aws_stack._resource_arn(pool_id, pattern, account_id=account_id, region_name=region_name)


def get_identitypool_arn(id, account_id=None, region_name=None):
    pattern = 'arn:aws:cognito-identity:%s:%s:identitypool/%s'
    return aws_stack._resource_arn(id, pattern, account_id=account_id, region_name=region_name)


def get_iot_policy_arn(id, account_id=None, region_name=None):
    pattern = 'arn:aws:iot:%s:%s:policy/%s'
    return aws_stack._resource_arn(id, pattern, account_id=account_id, region_name=region_name)


def get_iot_thing_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:iot:%s:%s:thing/%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def get_iot_thinggroup_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:iot:%s:%s:thinggroup/%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def get_iot_rule_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:iot:%s:%s:rule/%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def iotwireless_deviceprofile_arn(name, **kwargs):
    pattern = 'arn:aws:iotwireless:%s:%s:DeviceProfile/%s'
    return aws_stack._resource_arn(name, pattern, **kwargs)


def iotwireless_gateway_arn(name, **kwargs):
    pattern = 'arn:aws:iotwireless:%s:%s:WirelessGateway/%s'
    return aws_stack._resource_arn(name, pattern, **kwargs)


def iotwireless_device_arn(name, **kwargs):
    pattern = 'arn:aws:iotwireless:%s:%s:WirelessDevice/%s'
    return aws_stack._resource_arn(name, pattern, **kwargs)


def get_ecr_repository_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:ecr:%s:%s:repository/%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def analytics_application_arn(app_name, account_id=None, region_name=None):
    pattern = 'arn:aws:kinesisanalytics:%s:%s:application/%s'
    return aws_stack._resource_arn(app_name, pattern, account_id=account_id, region_name=region_name)


def batch_job_arn(job_id, account_id=None, region_name=None):
    pattern = 'arn:aws:batch:%s:%s:job/%s'
    return aws_stack._resource_arn(job_id, pattern, account_id=account_id, region_name=region_name)


def get_rds_subnet_group_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:rds:%s:%s:subgrp:%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def get_rds_cluster_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:rds:%s:%s:cluster:%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def get_rds_param_group_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:rds:%s:%s:pg:%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def get_rds_cluster_param_group_arn(name, account_id=None, region_name=None):
    pattern = 'arn:aws:rds:%s:%s:cluster-pg:%s'
    return aws_stack._resource_arn(name, pattern, account_id=account_id, region_name=region_name)


def get_rds_cluster_snapshot_arn(snap_id, account_id=None, region_name=None):
    pattern = 'arn:aws:rds:%s:%s:cluster-snapshot:rds:%s'
    return aws_stack._resource_arn(snap_id, pattern, account_id=account_id, region_name=region_name)


def get_elb_listener_arn(elb_id, listener_id, account_id=None, region_name=None):
    pattern = 'arn:aws:elasticloadbalancing:%s:%s:listener/%s'
    id = 'app/%s/%s' % (elb_id, listener_id)
    return aws_stack._resource_arn(id, pattern, account_id=account_id, region_name=region_name)


def get_elb_loadbalancer_arn(lb_name, lb_id, account_id=None, region_name=None):
    pattern = 'arn:aws:elasticloadbalancing:%s:%s:loadbalancer/%s'
    id = 'app/%s/%s' % (lb_name, lb_id)
    return aws_stack._resource_arn(id, pattern, account_id=account_id, region_name=region_name)


def amplify_app_arn(app_id, account_id=None, region_name=None):
    pattern = 'arn:aws:amplify:%s:%s:apps/%s'
    return aws_stack._resource_arn(app_id, pattern, account_id=account_id, region_name=region_name)


def amplify_branch_arn(app_id, branch_name, account_id=None, region_name=None):
    pattern = 'arn:aws:amplify:%s:%s:apps/{a}/branches/%s'.format(a=app_id)
    return aws_stack._resource_arn(branch_name, pattern, account_id=account_id, region_name=region_name)


def appsync_datasource_arn(api_id, source_name, account_id=None, region_name=None):
    pattern = 'arn:aws:appsync:%s:%s:apis/{a}/datasources/%s'.format(a=api_id)
    return aws_stack._resource_arn(source_name, pattern, account_id=account_id, region_name=region_name)


def appsync_type_arn(api_id, type_name, account_id=None, region_name=None):
    pattern = 'arn:aws:appsync:%s:%s:apis/{a}/types/%s'.format(a=api_id)
    return aws_stack._resource_arn(type_name, pattern, account_id=account_id, region_name=region_name)


def appsync_api_arn(api_id, account_id=None, region_name=None):
    pattern = 'arn:aws:appsync:%s:%s:apis/%s'
    return aws_stack._resource_arn(api_id, pattern, account_id=account_id, region_name=region_name)


def appsync_api_key_arn(api_id, api_key, account_id=None, region_name=None):
    pattern = 'arn:aws:appsync:%s:%s:apis/{api}/apikey/%s'.format(api=api_id)
    return aws_stack._resource_arn(api_key, pattern, account_id=account_id, region_name=region_name)


def appsync_resolver_arn(api_id, type_name, resolver_name, account_id=None, region_name=None):
    pattern = 'arn:aws:appsync:%s:%s:apis/{api}/types/{type_name}/resolvers/%s'.format(api=api_id, type_name=type_name)
    return aws_stack._resource_arn(resolver_name, pattern, account_id=account_id, region_name=region_name)


def appsync_function_arn(api_id, function_id, account_id=None, region_name=None):
    pattern = 'arn:aws:appsync:%s:%s:apis/{api}/functions/%s'.format(api=api_id)
    return aws_stack._resource_arn(function_id, pattern, account_id=account_id, region_name=region_name)


def scaling_policy_arn(policy_name, policy_id, service_ns, resource_id, account_id=None, region_name=None):
    pattern = 'arn:aws:autoscaling:%s:%s:scalingPolicy:{p}:resource/{ns}/{r}:policyName/%s'
    pattern = pattern.format(p=policy_id, ns=service_ns, r=resource_id)
    return aws_stack._resource_arn(policy_name, pattern, account_id=account_id, region_name=region_name)


def athena_data_catalog_arn(catalog_name, account_id=None, region_name=None):
    pattern = 'arn:aws:athena:%s:%s:datacatalog/%s'
    return aws_stack._resource_arn(catalog_name, pattern, account_id=account_id, region_name=region_name)


def athena_work_group_arn(catalog_name, account_id=None, region_name=None):
    pattern = 'arn:aws:athena:%s:%s:workgroup/%s'
    return aws_stack._resource_arn(catalog_name, pattern, account_id=account_id, region_name=region_name)


def ecs_service_arn(service_name, account_id=None, region_name=None):
    pattern = 'arn:aws:ecs:%s:%s:service/%s'
    return aws_stack._resource_arn(service_name, pattern, account_id=account_id, region_name=region_name)


def ecs_task_definition_arn(taskdef_name, version=1, account_id=None, region_name=None):
    pattern = 'arn:aws:ecs:%s:%s:task-definition/%s:{v}'.format(v=version)
    return aws_stack._resource_arn(taskdef_name, pattern, account_id=account_id, region_name=region_name)


def kafka_cluster_arn(cluster_name, account_id=None, region_name=None):
    pattern = 'arn:aws:kafka:%s:%s:cluster/%s'
    return aws_stack._resource_arn(cluster_name, pattern, account_id=account_id, region_name=region_name)


def kafka_configuration_arn(config_name, account_id=None, region_name=None):
    pattern = 'arn:aws:kafka:%s:%s:configuration/%s'
    return aws_stack._resource_arn(config_name, pattern, account_id=account_id, region_name=region_name)


def serverlessrepo_app_arn(app_name, account_id=None, region_name=None):
    pattern = 'arn:aws:serverlessrepo:%s:%s:applications/%s'
    return aws_stack._resource_arn(app_name, pattern, account_id=account_id, region_name=region_name)


def xray_sampling_rule_arn(rule_name, account_id=None, region_name=None):
    pattern = 'arn:aws:xray:%s:%s:sampling-rule/%s'
    return aws_stack._resource_arn(rule_name, pattern, account_id=account_id, region_name=region_name)


def elasticache_subnetgroup_arn(group_name, account_id=None, region_name=None):
    pattern = 'arn:aws:elasticache:%s:%s:subnetgroup:%s'
    return aws_stack._resource_arn(group_name, pattern, account_id=account_id, region_name=region_name)


def elasticache_securitygroup_arn(group_name, account_id=None, region_name=None):
    pattern = 'arn:aws:elasticache:%s:%s:securitygroup:%s'
    return aws_stack._resource_arn(group_name, pattern, account_id=account_id, region_name=region_name)


def elasticache_replicationgroup_arn(group_name, account_id=None, region_name=None):
    pattern = 'arn:aws:elasticache:%s:%s:replicationgroup:%s'
    return aws_stack._resource_arn(group_name, pattern, account_id=account_id, region_name=region_name)


def elasticache_parametergroup_arn(group_name, account_id=None, region_name=None):
    pattern = 'arn:aws:elasticache:%s:%s:parametergroup:%s'
    return aws_stack._resource_arn(group_name, pattern, account_id=account_id, region_name=region_name)


def elasticbeanstalk_application_arn(app_name, account_id=None, region_name=None):
    pattern = 'arn:aws:elasticbeanstalk:%s:%s:application/%s'
    return aws_stack._resource_arn(app_name, pattern, account_id=account_id, region_name=region_name)


def elasticbeanstalk_version_arn(app_name, version_label, account_id=None, region_name=None):
    pattern = 'arn:aws:elasticbeanstalk:%s:%s:applicationversion/{}/%s'.format(app_name)
    return aws_stack._resource_arn(version_label, pattern, account_id=account_id, region_name=region_name)


def cloudtrail_trail_arn(trail_name, account_id=None, region_name=None):
    pattern = 'arn:aws:cloudtrail:%s:%s:trail/%s'
    return aws_stack._resource_arn(trail_name, pattern, account_id=account_id, region_name=region_name)


def timestream_db_arn(db_name, account_id=None, region_name=None):
    pattern = 'arn:aws:timestream:%s:%s:database/%s'
    return aws_stack._resource_arn(db_name, pattern, account_id=account_id, region_name=region_name)


def timestream_db_table_arn(db_name, table_name, account_id=None, region_name=None):
    pattern = 'arn:aws:timestream:%s:%s:database/{}/table/%s'.format(db_name)
    return aws_stack._resource_arn(table_name, pattern, account_id=account_id, region_name=region_name)


def costexplorer_category_arn(cat_name, account_id=None, region_name=None):
    pattern = 'arn:aws:ce::%s:costcategory/%s'
    return aws_stack._resource_arn(cat_name, pattern, account_id=account_id, region_name=region_name)


def costexplorer_anomaly_subscription_arn(sub_id, account_id=None, region_name=None):
    pattern = 'arn:aws:ce::%s:anomalysubscription/%s'
    return aws_stack._resource_arn(sub_id, pattern, account_id=account_id, region_name=region_name)


def costexplorer_anomaly_monitor(mon_id, account_id=None, region_name=None):
    pattern = 'arn:aws:ce::%s:anomalymonitor/%s'
    return aws_stack._resource_arn(mon_id, pattern, account_id=account_id, region_name=region_name)


def servicediscovery_service_arn(service_id, account_id=None, region_name=None):
    pattern = 'arn:aws:servicediscovery:%s:%s:service/%s'
    return aws_stack._resource_arn(service_id, pattern, account_id=account_id, region_name=region_name)


def backup_vault_arn(vault_name, account_id=None, region_name=None):
    pattern = 'arn:aws:backup:%s:%s:backup-vault:%s'
    return aws_stack._resource_arn(vault_name, pattern, account_id=account_id, region_name=region_name)


def backup_plan_arn(plan_name, account_id=None, region_name=None):
    pattern = 'arn:aws:backup:%s:%s:backup-plan:%s'
    return aws_stack._resource_arn(plan_name, pattern, account_id=account_id, region_name=region_name)


def dynamodb_backup_arn(table_name, backup_name, account_id=None, region_name=None):
    pattern = 'arn:aws:dynamodb:%s:%s:table/{}/backup/%s'.format(table_name)
    return aws_stack._resource_arn(backup_name, pattern, account_id=account_id, region_name=region_name)
