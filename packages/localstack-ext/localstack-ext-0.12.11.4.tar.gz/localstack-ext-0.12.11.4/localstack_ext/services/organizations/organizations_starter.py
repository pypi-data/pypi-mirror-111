from localstack import config as localstack_config
from localstack.services import infra as localstack_infra


def apply_patches():
    # TODO
    pass


def start_organizations(port=None, asynchronous=False, update_listener=None):
    apply_patches()

    port = port or localstack_config.PORT_ORGANIZATIONS
    return localstack_infra.start_moto_server('organizations', port=port,
        update_listener=update_listener, name='Organizations', asynchronous=asynchronous)
