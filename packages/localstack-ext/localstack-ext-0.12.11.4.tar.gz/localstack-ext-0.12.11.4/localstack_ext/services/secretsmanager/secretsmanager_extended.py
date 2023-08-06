from moto.secretsmanager.models import secretsmanager_backends
from localstack.services.secretsmanager import secretsmanager_listener
from localstack_ext.services.base import MotoBackendPersistence


def patch_secretsmanager():
    persistence_mgr = MotoBackendPersistence('secretsmanager',
        update_listener=secretsmanager_listener.UPDATE_SECRETSMANAGER,
        backend_map=secretsmanager_backends)
    persistence_mgr.restore_and_setup_persistence()
