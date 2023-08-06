from localstack import config as localstack_config
from localstack.services.infra import start_local_api
from localstack_ext.services.transfer.transfer_api import serve


def start_transfer(port=None, asynchronous=False):
    port = port or localstack_config.PORT_TRANSFER
    return start_local_api('Transfer', port, api='transfer', method=serve, asynchronous=asynchronous)
