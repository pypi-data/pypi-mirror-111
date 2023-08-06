import json
import logging
from flask import Flask, request, jsonify
from localstack.services import generic_proxy
from localstack.utils.aws import aws_responses
from localstack.utils.common import to_str
from localstack_ext.bootstrap.ftp_server import add_ftp_user, update_ftp_user
from localstack_ext.services.transfer.models import TransferBackend
from localstack_ext.services.transfer.exceptions import ResourceNotFoundException

APP_NAME = 'transfer_api'

app = Flask(APP_NAME)

LOG = logging.getLogger(__name__)

FUNCTIONS_MAP = {
    'TransferService.CreateServer': 'create_server',
    'TransferService.DescribeServer': 'describe_server',
    'TransferService.DeleteServer': 'delete_server',
    'TransferService.ListServers': 'list_servers',
    'TransferService.CreateUser': 'create_user',
    'TransferService.UpdateUser': 'update_user',
    'TransferService.ImportSshPublicKey': 'import_ssh_public_key',
    'TransferService.DeleteSshPublicKey': 'delete_ssh_public_key',
    'TransferService.DescribeUser': 'describe_user',
    'TransferService.ListUsers': 'list_users',
    'TransferService.DeleteUser': 'delete_user'
}


def create_server(payload):
    backend = TransferBackend.get_region_backend()
    server_id = backend.create_server(**payload)

    return jsonify({
        'ServerId': server_id
    })


def describe_server(payload):
    backend = TransferBackend.get_region_backend()
    server = backend.describe_server(payload['ServerId'])
    return jsonify({
        'Server': server.as_json()
    })


def delete_server(payload):
    backend = TransferBackend.get_region_backend()
    backend.delete_server(payload['ServerId'])
    return jsonify({})


def list_servers(payload):
    backend = TransferBackend.get_region_backend()
    result = list(backend.servers.values())
    return jsonify({'Servers': result})


def create_user(payload):
    backend = TransferBackend.get_region_backend()
    server_id, user = backend.create_user(**payload)
    if not user:
        return aws_responses.flask_error_response_json(
            'InvalidRequestException.', 404, error_type='InvalidRequestException')

    port = int(server_id.split(':')[1])

    try:
        add_ftp_user(user, port)
    except Exception as e:
        LOG.info('Unable to add user "%s" to FTP server on port %s: %s' % (user, port, e))
        raise

    return jsonify({
        'ServerId': server_id,
        'UserName': user.username
    })


def update_user(payload):
    backend = TransferBackend.get_region_backend()
    server_id, user = backend.update_user(**payload)

    port = int(server_id.split(':')[1])

    update_ftp_user(user, port)

    return jsonify({
        'ServerId': server_id,
        'UserName': user.username
    })


def import_ssh_public_key(payload):
    backend = TransferBackend.get_region_backend()
    ssh_public_key_id = backend.import_ssh_public_key(**payload)

    return jsonify({
        'ServerId': payload['ServerId'],
        'UserName': payload['UserName'],
        'SshPublicKeyId': ssh_public_key_id
    })


def delete_ssh_public_key(payload):
    backend = TransferBackend.get_region_backend()
    backend.delete_ssh_public_key(**payload)

    return jsonify({})


def describe_user(payload):
    backend = TransferBackend.get_region_backend()
    server_id = payload['ServerId']
    user = backend.describe_user(server_id, payload['UserName'])

    return jsonify({
        'ServerId': server_id,
        'User': user.as_json()
    })


def list_users(payload):
    backend = TransferBackend.get_region_backend()
    server_id = payload['ServerId']
    users = backend.list_users(server_id)

    return jsonify({
        'ServerId': server_id,
        'Users': [
            user.as_short_json() for user in users
        ]
    })


def delete_user(payload):
    backend = TransferBackend.get_region_backend()
    backend.delete_user(payload['ServerId'], payload['UserName'])
    return jsonify({})


@app.route('/', methods=['POST'])
def handle_request():
    payload = json.loads(to_str(request.get_data()))
    action = request.headers.get('X-Amz-Target', '')
    func = globals().get(FUNCTIONS_MAP.get(action, ''))

    if not func:
        LOG.warning('Unable to find Transfer API method for target header %s' % action)

    try:
        return func(payload)

    except ResourceNotFoundException:
        return aws_responses.flask_error_response_json(
            'The resource you requested does not exist.', 404, error_type='ResourceNotFoundException')
    except Exception as e:
        return aws_responses.flask_error_response_json(
            'Internal server error: %s' % e, 500, error_type='InternalServerError')


def serve(port, quiet=True):
    generic_proxy.serve_flask_app(app=app, port=port, quiet=quiet)
