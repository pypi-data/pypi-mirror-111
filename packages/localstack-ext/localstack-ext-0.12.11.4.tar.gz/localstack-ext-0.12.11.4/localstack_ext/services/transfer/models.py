import uuid
from datetime import datetime
from localstack.utils.aws import aws_stack
from localstack_ext.bootstrap import ftp_server
from localstack_ext.services.transfer.exceptions import ResourceNotFoundException
from localstack_ext.utils.common import get_available_service_instance_port

server_arn_pattern = 'arn:aws:transfer:%s:%s:server/%s'
user_arn_pattern = 'arn:aws:transfer:%s:%s:user/%s'

REGIONS = {}


def _random(pattern, length):
    return pattern.format(str(uuid.uuid4()).replace('-', ''))[:length]


def _generate_server_id(port):
    # TODO include port number in server_id
    return 's-{}:{}'.format(str(uuid.uuid4()).replace('-', '')[:13], port)


def _start_ftp_server():
    port = get_available_service_instance_port()
    thread = ftp_server.start_ftp(port)
    return port, thread


class TransferBackend(object):
    def __init__(self):
        self.servers = {}

    def create_server(self, **kws):
        # TODO currently just support FTP protocol
        port, thread = _start_ftp_server()

        server = Server(port, **kws)
        self.servers[server.id] = server
        server._thread = thread

        return server.id

    def describe_server(self, server_id):
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        return self.servers[server_id]

    def delete_server(self, server_id):
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        server = self.servers.pop(server_id)
        try:
            server._thread and server._thread.stop()
        except Exception:
            pass
        server._thread = None

    def create_user(self, **kws):
        server_id = kws['ServerId']
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        server = self.servers[server_id]
        if server.identity_provider_type != 'SERVICE_MANAGED':
            return server_id, None

        user = User(**kws)
        self.servers[server_id].users[kws['UserName']] = user

        return server_id, user

    def update_user(self, **kws):
        server_id = kws['ServerId']
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        username = kws['UserName']
        if username not in self.servers[server_id].users:
            raise ResourceNotFoundException()

        user = self.servers[server_id].users[username]
        user.update(**kws)

        return server_id, user

    def import_ssh_public_key(self, **kws):
        server_id = kws['ServerId']
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        username = kws['UserName']
        if username not in self.servers[server_id].users:
            raise ResourceNotFoundException()

        ssh_public_key_id = _random('s-{}', 21)
        self.servers[server_id].users[username].ssh_public_keys[ssh_public_key_id] = {
            'SshPublicKeyId': ssh_public_key_id,
            'DateImported': datetime.now(),
            'SshPublicKeyBody': kws['SshPublicKeyBody']
        }

        return ssh_public_key_id

    def delete_ssh_public_key(self, **kws):
        server_id = kws['ServerId']
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        username = kws['UserName']
        if username not in self.servers[server_id].users:
            raise ResourceNotFoundException()

        self.servers[server_id].users[username].ssh_public_keys.pop(kws['SshPublicKeyId'], None)

    def describe_user(self, server_id, username):
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        if username not in self.servers[server_id].users:
            raise ResourceNotFoundException()

        return self.servers[server_id].users[username]

    def list_users(self, server_id):
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        return [user for user in self.servers[server_id].users.values()]

    def delete_user(self, server_id, username):
        if server_id not in self.servers:
            raise ResourceNotFoundException()

        if username not in self.servers[server_id].users:
            raise ResourceNotFoundException()

        self.servers[server_id].users.pop(username)
        return username

    @classmethod
    def get_region_backend(cls):
        region = aws_stack.get_region()
        instance = REGIONS[region] = REGIONS.get(region) or TransferBackend()
        return instance


class Server(object):
    def __init__(self, port, **kws):
        self.id = _generate_server_id(port)
        self.certificate = kws.get('Certificate', '')
        self.endpoint_type = kws.get('EndpointType', '')
        self.host_key = kws.get('HostKey', '')
        self.identity_provider_type = kws.get('IdentityProviderType', 'SERVICE_MANAGED')
        self.logging_role = kws.get('LoggingRole', '')
        self.protocols = kws.get('Protocols', ['FTP'])
        self.users = {}
        self.tags = kws.get('Tags', [])
        self._thread = None

    def as_json(self):
        return {
            'ServerId': self.id,
            'Arn': aws_stack._resource_arn(self.id, server_arn_pattern),
            'Certificate': self.certificate,
            'EndpointType': self.endpoint_type,
            'HostKeyFingerprint': '',
            'IdentityProviderType': self.identity_provider_type,
            'LoggingRole': self.logging_role,
            'Protocols': self.protocols,
            'State': 'ONLINE',
            'UserCount': len(self.users.keys()),
            'Tags': self.tags
        }


class User(object):
    def __init__(self, **kws):
        self.username = kws['UserName']
        self.home_directory = kws.get('HomeDirectory', '/')
        self.home_directory_type = kws.get('HomeDirectoryType', 'PATH')
        self.home_directory_mappings = kws.get('HomeDirectoryMappings', [])
        self.policy = kws.get('Policy', {})
        self.role = kws.get('Role', '')

        self.ssh_public_keys = {}
        if 'SshPublicKeyBody' in kws:
            ssh_public_key_id = _random('s-{}', 21)
            self.ssh_public_keys[ssh_public_key_id] = {
                'SshPublicKeyId': ssh_public_key_id,
                'DateImported': datetime.now(),
                'SshPublicKeyBody': kws['SshPublicKeyBody']
            }

        self.tags = kws.get('Tags', [])

    def update(self, **kws):
        self.home_directory = kws.get('HomeDirectory', self.home_directory)
        self.home_directory_type = kws.get('HomeDirectoryType', self.home_directory_type)
        self.home_directory_mappings = kws.get('HomeDirectoryMappings', self.home_directory_mappings)
        self.policy = kws.get('Policy', self.policy)
        self.role = kws.get('Role', self.role)

    def as_json(self):
        return {
            'Arn': aws_stack._resource_arn(self.username, user_arn_pattern),
            'UserName': self.username,
            'HomeDirectory': self.home_directory,
            'HomeDirectoryType': self.home_directory_type,
            'HomeDirectoryMappings': self.home_directory_mappings,
            'Policy': self.policy,
            'Role': self.role,
            'SshPublicKeys': [public_key for public_key in self.ssh_public_keys.values()],
            'Tags': self.tags
        }

    def as_short_json(self):
        return {
            'Arn': aws_stack._resource_arn(self.username, user_arn_pattern),
            'UserName': self.username,
            'HomeDirectory': self.home_directory,
            'HomeDirectoryType': self.home_directory_type,
            'Role': self.role,
            'SshPublicKeyCount': len(self.ssh_public_keys.keys())
        }

    def get_directory_configuration(self):
        return {
            'HomeDirectory': self.home_directory,
            'HomeDirectoryType': self.home_directory_type,
            'HomeDirectoryMappings': self.home_directory_mappings
        }
