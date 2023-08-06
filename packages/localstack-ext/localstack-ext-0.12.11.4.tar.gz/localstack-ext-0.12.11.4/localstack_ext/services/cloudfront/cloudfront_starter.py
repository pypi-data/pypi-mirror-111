from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack_ext.services.cloudfront import cloudfront_api


def start_cloudfront(port=None, asynchronous=False, update_listener=None):
    if not port:
        port = localstack_config.PORT_CLOUDFRONT

    # initialize persistence mechanism
    cloudfront_api.CloudFrontState.restore_and_setup_persistence('cloudfront')

    return localstack_infra.start_local_api('CloudFront', port, api='cloudfront',
        method=cloudfront_api.serve, asynchronous=asynchronous)
