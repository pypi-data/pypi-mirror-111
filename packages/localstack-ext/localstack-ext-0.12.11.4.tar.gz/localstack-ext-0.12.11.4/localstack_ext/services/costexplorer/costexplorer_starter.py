from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack_ext.services.costexplorer import costexplorer_api


def start_costexplorer(port=None, asynchronous=False, update_listener=None):
    port = port or localstack_config.PORT_CE

    # restore state and set up persistence handlers
    costexplorer_api.CostExplorerRegion.restore_and_setup_persistence('ce')

    return localstack_infra.start_local_api('Cost Explorer', port, api='ce',
        method=costexplorer_api.serve, asynchronous=asynchronous)
