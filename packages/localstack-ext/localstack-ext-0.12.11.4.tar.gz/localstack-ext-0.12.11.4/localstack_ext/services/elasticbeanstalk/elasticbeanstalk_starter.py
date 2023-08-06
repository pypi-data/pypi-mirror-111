from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack_ext.services.elasticbeanstalk import elasticbeanstalk_api


def start_elasticbeanstalk(port=None, asynchronous=False, update_listener=None):
    port = port or localstack_config.PORT_ELASTICBEANSTALK
    return localstack_infra.start_local_api('ElasticBeanstalk', port, api='elasticbeanstalk',
        method=elasticbeanstalk_api.serve, asynchronous=asynchronous)
