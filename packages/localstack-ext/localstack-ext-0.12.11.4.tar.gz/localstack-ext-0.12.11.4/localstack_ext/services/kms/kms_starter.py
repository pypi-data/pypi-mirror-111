import logging
from moto.kms.models import kms_backends
from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack_ext.services.base import prepare_and_load_persistence_for_moto_backend

LOG = logging.getLogger(__name__)

# TODO: Remove this file - already covered in upstream repo!


def start_kms(port=None, asynchronous=False, update_listener=None):
    if not port:
        port = localstack_config.PORT_KMS

    # setup and restore persistence
    prepare_and_load_persistence_for_moto_backend('kms', kms_backends)

    return localstack_infra.start_moto_server(
        'kms', port=port, update_listener=update_listener, name='KMS', asynchronous=asynchronous)
