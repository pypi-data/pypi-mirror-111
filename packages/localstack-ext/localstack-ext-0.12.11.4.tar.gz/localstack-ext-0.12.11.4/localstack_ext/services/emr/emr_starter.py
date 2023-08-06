from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack_ext import config as ext_config
from localstack_ext.utils.hadoop import start_hadoop_spark_container

# port lazily initialized on startup
PORT_EMR_BACKEND = None


def start_emr(port=None, asynchronous=False, update_listener=None):
    global PORT_EMR_BACKEND
    port = port or localstack_config.PORT_EMR
    if ext_config.AUTOSTART_UTIL_CONTAINERS:
        start_hadoop_spark_container()
    PORT_EMR_BACKEND = localstack_infra.get_multiserver_or_free_service_port()
    return localstack_infra.start_moto_server('emr', port=port, backend_port=PORT_EMR_BACKEND,
        update_listener=update_listener, name='EMR', asynchronous=asynchronous)
