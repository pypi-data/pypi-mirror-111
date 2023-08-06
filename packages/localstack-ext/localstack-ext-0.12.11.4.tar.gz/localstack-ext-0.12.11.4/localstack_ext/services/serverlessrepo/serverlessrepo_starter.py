from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack_ext.services.serverlessrepo import serverlessrepo_api


def start_serverlessrepo(port=None, asynchronous=False, update_listener=None):
    port = port or localstack_config.PORT_SERVERLESSREPO

    # initialize persistence mechanism
    serverlessrepo_api.ServerlessRepoRegion.restore_and_setup_persistence('serverlessrepo')

    return localstack_infra.start_local_api('Serverless Application Repository', port, api='serverlessrepo',
        method=serverlessrepo_api.serve, asynchronous=asynchronous)
