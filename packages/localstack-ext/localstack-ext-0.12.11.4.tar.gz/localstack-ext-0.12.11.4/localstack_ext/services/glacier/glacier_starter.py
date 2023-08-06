from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack.services.infra import get_multiserver_or_free_service_port


def start_glacier(port=None, asynchronous=False, update_listener=None):
    port = port or localstack_config.PORT_GLACIER
    backend_port = get_multiserver_or_free_service_port()
    return localstack_infra.start_moto_server('glacier', port=port, backend_port=backend_port,
        update_listener=update_listener, name='Glacier', asynchronous=asynchronous)
