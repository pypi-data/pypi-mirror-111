import types
import logging
from moto.sns.models import sns_backends
from requests.models import Request, Response
from localstack.services.sns import sns_listener
from localstack.utils import persistence
from localstack_ext.services.base import prepare_and_load_persistence_for_moto_backend
from localstack_ext.utils import persistence as persistence_ext

return_response_orig = sns_listener.UPDATE_SNS.return_response
forward_request_orig = sns_listener.UPDATE_SNS.forward_request

LOG = logging.getLogger(__name__)


def forward_request(self, method, path, data, headers):
    data_orig = data
    # transform identifiers for persisted data
    data = persistence_ext.transform_incoming_data('sns', data, url_encoded=True)

    result = forward_request_orig(method, path, data, headers)

    if isinstance(result, (int, dict, Request, Response)):
        return result

    if data_orig != data:
        return Request(data=data, headers=headers, method=method)

    return result


def return_response(self, method, path, data, headers, response):
    result = return_response_orig(method, path, data, headers, response=response)

    # TODO still needed?

    # persist this API call to disk
    recorded_response = result if isinstance(result, Response) else response
    persistence.record('sns', method, path, data, headers, response=recorded_response)

    # transform identifiers for persisted data
    persistence_ext.transform_outgoing_data('sns', recorded_response)

    return result


def patch_sns():
    # patch existing listener methods
    sns_listener.UPDATE_SNS.forward_request = types.MethodType(forward_request, sns_listener.UPDATE_SNS)
    sns_listener.UPDATE_SNS.return_response = types.MethodType(return_response, sns_listener.UPDATE_SNS)

    # restore state and set up persistence handlers
    sns_listener.SNSBackend.restore_and_setup_persistence('sns')
    prepare_and_load_persistence_for_moto_backend('sns', sns_backends)
