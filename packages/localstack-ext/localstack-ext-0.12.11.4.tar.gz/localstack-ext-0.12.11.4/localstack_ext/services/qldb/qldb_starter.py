from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack_ext.services.qldb import qldb_api


def start_qldb(port=None, asynchronous=False, update_listener=None):
    port = port or localstack_config.PORT_QLDB

    # initialize persistence mechanism
    qldb_api.QLDBRegion.restore_and_setup_persistence('qldb')

    return localstack_infra.start_local_api('QLDB', port, api='qldb',
        method=qldb_api.serve, asynchronous=asynchronous)
