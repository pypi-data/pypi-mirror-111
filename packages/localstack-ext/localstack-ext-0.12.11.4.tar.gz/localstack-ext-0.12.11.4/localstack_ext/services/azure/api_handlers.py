import os
import re
import json
import logging
import functools
import xmltodict
from requests.models import Response
from localstack import config
from localstack.utils.common import (
    short_uid, to_str, timestamp_millis, new_tmp_file, save_file, mkdir, unzip,
    get_free_tcp_port, run, rm_docker_container)
from localstack.utils.aws.aws_responses import requests_response
from localstack_ext import config as ext_config
from localstack_ext.utils.common import assign_to_path
from localstack_ext.services.azure.azure_utils import (
    get_azure_endpoint, get_azure_host, REGIONS, get_scm_url, get_ftp_host)
from localstack_ext.services.azure.crud_handler import handle_request_for_method, lookup_resource

LOG = logging.getLogger('localstack_ext.services.azure.api_handlers')

REGEX_FLAGS = re.DOTALL | re.IGNORECASE

IMAGE_BASE = 'mcr.microsoft.com/azure-functions'
FUNCTION_RUNTIMES = ['dotnet', 'node', 'powershell', 'java', 'python', 'base']


class APIHandler(object):
    """ Base class for API handlers. """

    INSTANCES = {}

    def handle_request(self, req):
        methods = self.api_methods()
        matching = [m for m in methods if m._matches_request(req)]
        if len(matching) > 1:
            raise Exception('Found multiple API methods matching request %s %s: %s' % (req.method, req.path, matching))
        if not matching:
            # fall back to default request handling (generic CRUD request handler)
            return handle_request_for_method(req)
        result = matching[0](req)
        if isinstance(result, Response):
            return result
        headers = {}
        data = result
        status = 200
        if isinstance(result, tuple):
            if len(result) > 2:
                data, status, headers = result
            elif len(result) > 1:
                data, status = result
        if isinstance(data, int):
            status = data
            data = '{}'
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        return requests_response(data, headers=headers, status_code=status)

    def handle_request_generic(self, req):
        # TODO: extract models from class
        return handle_request_for_method(req)

    @classmethod
    def get(cls, api=None):
        api = api or '_generic_'
        if not cls.INSTANCES:
            for clazz in cls.__subclasses__():
                cls.INSTANCES[clazz.api()] = clazz()
            cls.INSTANCES['_generic_'] = APIHandler()
        return cls.INSTANCES.get(api)

    def api_methods(self):
        methods = [getattr(self, m) for m in dir(self) if not m.startswith('__')]
        result = [m for m in methods if hasattr(m, '_matches_request')]
        return result


def handler(method=None, path=None, payload=None):
    """ Decorator used to match incoming requests against API handler methods. """
    def _matches_request(req):
        path_pattern = req.spec.path_pattern if req.spec else req.path_to_match
        path_pattern = path_pattern.split('?')[0]
        # TODO: add matching for path params
        pairs = ((method, req.method), (path, path_pattern), (payload, req.data))
        for pair in pairs:
            if pair[0] and not re.match(pair[0], to_str(pair[1]), flags=REGEX_FLAGS):
                return False
        return True

    def _decorator(wrapped):
        @functools.wraps(wrapped)
        def _wrapper(*args, **kwargs):
            return wrapped(*args, **kwargs)
        _wrapper._matches_request = _matches_request
        return _wrapper
    return _decorator


# -------------
# API HANDLERS
# -------------

class TenantMetadata(APIHandler):
    @staticmethod
    def api():
        return 'tenant-discovery'

    @handler(method='GET', path=r'^/common/discovery/instance.*')
    def get_oidc_metadata(self, req):
        oidc_config = '%s/common/.well-known/openid-configuration' % get_azure_endpoint()
        result = {
            'tenant_discovery_endpoint': oidc_config,
            'api-version': '1.1',
            'metadata': [{
                'preferred_network': ext_config.LOCAL_HOSTNAME,
                'preferred_cache': ext_config.LOCAL_HOSTNAME,
                'aliases': []
            }]
        }
        return result

    @handler(method='POST', path=r'^/[^/]+/oauth2/([^/]+/)?token')
    def oauth2_token(self, req):
        claims = {'sub': 'user123', 'iss': get_azure_endpoint(),
            'tid': 'tenant1', 'aud': 'client1', 'preferred_username': 'user123'}
        result = {'token_type': 'bearer', 'access_token': 'token123',
            'expires_in': 60 * 60 * 24, 'id_token_claims': claims}
        return result

    @handler(method='POST', path=r'^/[^/]+/oauth2/([^/]+/)?devicecode')
    def oauth2_devicecode(self, req):
        url = '%s/common/oauth2/devicecode' % get_azure_endpoint()
        result = {
            'user_code': 'user123', 'device_code': 'code123', 'interval': 5, 'verification_url': url,
            'message': 'Enter code "code123" here to authenticate: %s' % url, 'expires_in': '900'
        }
        return result

    @handler(method='GET', path=r'^/common([^/]+/)?/.well-known/openid-configuration')
    def openid_config(self, req):
        endpoint = get_azure_endpoint()
        result = {
            'token_endpoint': '%s/common/oauth2/token' % endpoint,
            'jwks_uri': '%s/common/discovery/keys' % endpoint,
            'authorization_endpoint': '%s/common/oauth2/authorize' % endpoint,
            'device_authorization_endpoint': '%s/common/oauth2/devicecode' % endpoint
        }
        return result

    @handler(method='GET', path=r'^/common/UserRealm/.*')
    def get_user_realm(self, req):
        result = {
            'ver': '1.0', 'account_type': 'Managed', 'domain_name': ext_config.LOCAL_HOSTNAME
        }
        return result

    @handler(method='GET', path=r'^/subscriptions$')
    def list_subscriptions(self, req):
        sub_id = 'sub123'  # TODO hardcoded for now
        test_sub = {
            'subscriptionId': sub_id, 'id': '/subscriptions/%s' % sub_id,
            'displayName': 'Test Subscription', 'state': 'Enabled', 'managedByTenants': []
        }
        result = {'value': [test_sub]}
        return result

    @handler(method='GET', path=r'^/tenants$')
    def list_tenants(self, req):
        tenant_id = 'tenant123'  # TODO hardcoded for now
        result = {
            'value': [{'id': '/tenants/%s' % tenant_id, 'tenantId': tenant_id, 'name': 'Test Tenant'}]
        }
        return result

    @handler(method='GET', path=r'^/arm/cloud/metadata')
    def arm_cloud_metadata(self, req):
        azure_endpoint = get_azure_endpoint()
        azure_host = get_azure_host()
        result = [{
            'portal': azure_endpoint,
            'authentication': {
                'loginEndpoint': azure_endpoint,
                'audiences': [azure_endpoint],
                'tenant': 'common',
                'identityProvider': 'AAD'
            },
            'name': 'AzureCloud',
            'suffixes': {
                'azureDataLakeStoreFileSystem': azure_host,
                'acrLoginServer': azure_host,
                'sqlServerHostname': azure_host,
                'azureDataLakeAnalyticsCatalogAndJob': azure_host,
                'keyVaultDns': azure_host,
                'storage': azure_host,
                'azureFrontDoorEndpointSuffix': azure_host
            },
            'resourceManager': azure_endpoint,
            'sqlManagement': azure_endpoint
        }]
        return result


class EventHubs(APIHandler):
    @staticmethod
    def api():
        return 'eventhub-hubs'

    # @handler(method='PUT', path=r'.*/providers/Microsoft.EventHub/eventhubs.*')
    # def add_eventhub(self, req):
    #     result = {}
    #     return result


class EventHubAuthRules(APIHandler):
    @staticmethod
    def api():
        return 'eventhub-authrules'


class EventHubConsumerGroups(APIHandler):
    @staticmethod
    def api():
        return 'eventhub-consumergroups'


class EventHubNamespaces(APIHandler):
    @staticmethod
    def api():
        return 'eventhub-namespaces'

    # @handler(method='PUT', path=r'.*/providers/Microsoft.EventHub/namespaces.*')
    # def add_namespace(self, req):
    #     result = {}
    #     return result


class StorageBlob(APIHandler):
    @staticmethod
    def api():
        return 'storage-blob'


class ServiceBus(APIHandler):
    @staticmethod
    def api():
        return 'servicebus'


class ResourceGraph(APIHandler):
    @staticmethod
    def api():
        return 'resource-graph'

    @handler(method='POST', path=r'.*providers/Microsoft.ResourceGraph/resources')
    def query_resources(self, req):
        content = req.content()
        query = content.get('query')
        LOG.info('Running resource graph query: %s' % query)

        # TODO implement proper query engine!
        records = []
        match = re.match(r"where type =~ 'Microsoft.Web/sites' and name =~ '([^']+)' | project id", query)
        if match:
            sub_id = content.get('subscriptions')[0]
            rg_name = 'g1'  # TODO look up proper resource group name!
            app_id = match.group(1)
            id = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Web/sites/%s' % (sub_id, rg_name, app_id)
            records = [{'id': id}]

        # prepare columns
        cols = set()
        for r in records:
            [cols.add(k) for k in r.keys()]
        cols = list(cols)

        result = {
            'totalRecords': len(records),
            'count': len(records),
            'resultTruncated': 'false',
            'data': {
                'columns': [{
                    'name': col, 'type': 'string'  # TODO: add proper types
                } for col in cols],
                'rows': [
                    [r.get(col) for col in cols] for r in records
                ]
            }
        }
        return result


class WebApps(APIHandler):
    @staticmethod
    def api():
        return 'web-apps'

    @staticmethod
    def models():
        ID_PATTERN = '[a-zA-Z0-9_-]+'
        return {
            'web-app-settings': ['Microsoft.Web/sites/%s/config/AppSettings' % ID_PATTERN]
        }

    @handler(method='PUT', path=r'.*providers/Microsoft.Web/sites/[^/]+$')
    def create_web_app(self, req):
        add_req_params_to_request(req, {'properties.resourceGroup': 'resourceGroupName'})
        azure_host = get_azure_host()
        site_id = req.path_without_query().rpartition('/')[2]
        azure_host_scm = get_scm_url(site_id).split('://')[-1]
        hostnames = [{
            'name': host,
            'sslState': 'SniEnabled',
            'thumbprint': 'IUAHSIUHASD78ASDIUABFKASF79ASUASD8ASFHOANKSL',
            'toUpdate': True,
            'hostType': type
        } for host, type in {azure_host_scm: 'Repository', azure_host: 'Standard'}.items()]
        if not req.content().get('properties', {}).get('serverFarmId'):
            service_plan = self.lookup_service_plan(req)
            if service_plan:
                add_values_to_request(req, {'properties.serverFarmId': service_plan.get('id')})
        add_values_to_request(req, {'properties.hostNameSslStates': hostnames})
        add_values_to_request(req, {'properties.enabledHostNames': [azure_host_scm, azure_host]})
        return self.handle_request_generic(req)

    @handler(method='GET', path=r'.*Microsoft.Web/sites/[^/]+/config/web')
    def get_web_app_configuration(self, req):
        result = self.handle_request_generic(req)
        if result.status_code == 404:
            result = {'id': req.path_without_query(), 'properties': {}}
        return result

    @handler(method='GET', path=r'.*Microsoft.Web/sites/[^/]+/config/slotConfigNames')
    def get_slot_config_name(self, req):
        result = {'properties': {
            'appSettingNames': [], 'azureStorageConfigNames': [], 'connectionStringNames': []
        }}
        return result

    @handler(method='POST', path=r'.*Microsoft.Web/sites/[^/]+/config/appsettings/list')
    def list_app_settings(self, req):
        app_name = req.get_path_params().get('name')
        # TODO: extract subscription and resourceGroup from path as well
        result = self.get_app_settings(app_name)
        return result

    @handler(method='POST', path=r'.*Microsoft.Web/sites/[^/]+/config/publishingcredentials/list')
    def list_publishing_credentials(self, req):
        app_name = req.get_path_params().get('name')
        result = {'name': 'test', 'type': 'Microsoft.Web/sites/publishingcredentials',
            'properties': {
                'publishingUserName': 'test', 'publishingPassword': 'test',
                'scmUri': get_scm_url(app_name), 'isDeleted': False
            }
        }
        return result

    @handler(method='POST', path=r'.*Microsoft.Web/sites/[^/]+/config/ConnectionStrings/list')
    def list_connection_strings(self, req):
        result = {
            'id': re.sub(r'(.*/config/ConnectionStrings).*', r'\1', req.path, flags=REGEX_FLAGS),
            'type': 'Microsoft.Web/sites/config',
            'properties': {
                # TODO add strings
            }
        }
        return result

    @handler(method='POST', path=r'.*providers/Microsoft.Web/sites/.+/publishxml')
    def list_publishing_profile_xml(self, req):
        endpoint = {
            '@publishMethod': 'FTP',
            '@publishUrl': get_ftp_host(),
            '@userName': 'test', '@userPWD': 'test',
            'databases': {}
        }
        result = {
            'publishData': {
                'publishProfile': [endpoint, endpoint]
            }
        }
        return xmltodict.unparse(result), 200

    @staticmethod
    def get_app_settings(app_id):
        suffix = 'Microsoft.Web/sites/%s/config/AppSettings' % app_id
        result = lookup_resource('web-app', id_suffix=suffix)
        if not result:
            result = {'properties': {}}
        return result

    @staticmethod
    def lookup_service_plan(req):
        prefix = req.path_without_query().split('/Microsoft.Web/')[0]
        prefix = '%s/Microsoft.Web/serverfarms' % prefix
        result = lookup_resource('service-plans', id_prefix=prefix)
        return result


class SourceControl(APIHandler):
    @staticmethod
    def api():
        return 'scm'

    @handler(method='GET', path=r'(/api)?/settings')
    def get_settings(self, req):
        result = {}
        app_id = self.get_app_id_from_host(req)
        if app_id:
            # look up settings in app details
            suffix = 'Microsoft.Web/sites/%s' % app_id
            matching = lookup_resource('web-app', id_suffix=suffix)
            if matching:
                settings = matching.get('properties', {}).get('siteConfig', {}).get('appSettings', [])
                settings = {entry['name']: entry['value'] for entry in settings}
                result.update(settings)
            # look up app settings
            matching = WebApps.get_app_settings(app_id) or {}
            result.update(matching.get('properties', {}))
        return result

    @handler(method='GET', path=r'(/api)?/deployments(/[^/]+)?$')
    def get_deployments(self, req):
        result = {'id': 'latest', 'status': 4}
        path = req.path_without_query()
        if path.endswith('/deployments'):
            result = [result]
        else:
            result['id'] = path.rpartition('/deployments/')[2]
        return result

    @handler(method='GET', path=r'(/api)?/deployments/[^/]+/log$')
    def get_deployment_logs(self, req):
        result = [{'log_time': timestamp_millis(), 'message': 'Test Logs ...', 'details_url': None}]
        return result

    @handler(method='POST', path=r'(/api)?/zipdeploy')
    def deploy_zip_file(self, req):
        result = {}
        app_id = self.get_app_id_from_host(req)
        if not app_id:
            return {}
        func_folder = self.local_function_folder(app_id)
        func_zip_file = new_tmp_file()
        save_file(func_zip_file, req.data)
        unzip(func_zip_file, func_folder)
        self.start_function_container(app_id)
        return result

    @staticmethod
    def get_app_id_from_host(req):
        host = req.host()
        if '.scm.' not in host:
            return
        app_id = host.split('.scm.')[0]
        return app_id

    @classmethod
    # TODO: move to separate file, refactor logic!
    def start_function_container(cls, app_id):
        azure_endpoint = get_azure_endpoint()
        conn_str = ('DefaultEndpointsProtocol=http;BlobEndpoint=%s/devstoreaccount1;' +
            'AccountName=devstoreaccount1;AccountKey=test') % azure_endpoint
        # TODO extract function runtime from config!
        runtime = 'python'
        docker_img = cls.function_image(runtime)
        func_folder = cls.local_function_folder(app_id)
        port = get_free_tcp_port()
        container_name = 'ls-az-func-%s' % app_id
        cmd = ('%s run --rm -d -v %s:/home/site/wwwroot --name %s ' +
            '-e AzureFunctionsJobHost__Logging__Console__IsEnabled=true ' +
            '-e AzureWebJobsStorage="%s" -it -p %s:80 %s') % (
                config.DOCKER_CMD, func_folder, container_name, conn_str, port, docker_img)
        # terminate existing container (if it exists)
        rm_docker_container(container_name, check_existence=True)
        # start new container
        run(cmd)
        LOG.info('Starting Docker container for Azure function App ID %s: %s' % (app_id, cmd))
        result = {}
        return result

    @staticmethod
    def local_function_folder(app_name):
        result = os.path.join(config.TMP_FOLDER, 'azure-funcs', app_name)
        mkdir(result)
        return result

    @staticmethod
    def function_image(runtime):
        return '%s/%s' % (IMAGE_BASE, runtime)


class ServicePlans(APIHandler):
    @staticmethod
    def api():
        return 'service-plans'

    @handler(method='PUT', path=r'.*providers/Microsoft.Web/serverfarms.*')
    def add_service_plan(self, req):
        add_values_to_request(req, {'id': req.path_without_query()})
        result = self.handle_request_generic(req)
        result.status_code = 200
        return result


class StorageAccounts(APIHandler):
    @staticmethod
    def api():
        return 'storage-accounts'

    @handler(method='POST', path=r'.*providers/Microsoft.Storage/storageAccounts/[^/]*/listKeys.*')
    def list_keys(self, req):
        # TODO hardcoded for now
        result = {'keys': [
            {'keyName': 'key1', 'permissions': 'Full', 'value': 'keyvalue123'},
            {'keyName': 'key2', 'permissions': 'Full', 'value': 'keyvalue456'}
        ]}
        return result

    @handler(method='PUT', path=r'.*providers/Microsoft.Storage/storageAccounts.*')
    def add_service_plan(self, req):
        endpoint = get_azure_endpoint()
        values = {
            'properties.primaryEndpoints.blob': endpoint,
            'properties.primaryEndpoints.file': endpoint,
            'properties.primaryEndpoints.table': endpoint,
            'properties.primaryEndpoints.queue': endpoint
        }
        add_values_to_request(req, values)
        result = self.handle_request_generic(req)
        return result


class WebResources(APIHandler):
    @staticmethod
    def api():
        return 'web-resources'

    @handler(method='POST', path=r'.*providers/Microsoft.Web/validate')
    def validate_service_plan(self, req):
        data = {'status': 'ok'}
        return data

    @handler(method='GET', path=r'.*providers/Microsoft.Web/geoRegions')
    def list_geo_regions(self, req):
        path = req.path_without_query()
        result = {'value': [{
            'id': '%s/%s' % (path, r), 'name': r, 'type': 'Microsoft.Web/geoRegions', 'properties': {'name': r}
        } for r in REGIONS]}
        return result


class StorageQueue(APIHandler):
    QUEUES = {}

    @staticmethod
    def api():
        return 'storage-queue'

    @handler(method='POST', path=r'^/[^/]+/messages')
    def add_message(self, req):
        content = req.content()
        msg_text = content.get('QueueMessage', {}).get('MessageText')
        queue = self._queue(req)
        msg = {'MessageId': short_uid(), 'MessageText': msg_text, 'PopReceipt': short_uid(), 'DequeueCount': 0}
        queue.insert(0, msg)
        data = {'Enqueued': msg}
        return xmltodict.unparse(data), 201

    @handler(method='GET', path=r'^/[^/]+/messages.*')
    def get_messages(self, req):
        queue = self._queue(req)
        # TODO: read numofmessages query param!
        messages = queue[-1:]
        data = {'QueueMessagesList': {'QueueMessage': messages}}
        return xmltodict.unparse(data), 200

    @handler(method='DELETE', path=r'^/[^/]+/messages/[^/]+$')
    def delete_messages(self, req):
        queue = self._queue(req)
        # msg_id = req.get_path_params().get('messageid')  # TODO
        msg_id = self._path_params(req)[2]
        for m in queue:
            if m['MessageId'] == msg_id:
                # TODO: check validity of "popreceipt" query param!
                queue.remove(m)
                break
        return '', 204

    @handler(method='DELETE', path=r'^/[^/]+$')
    def delete_queue(self, req):
        result = self.handle_request_generic(req)
        result.status_code = 204
        return result

    def _queue_name(self, req):
        return self._path_params(req)[0]

    def _queue(self, req):
        queue_name = self._queue_name(req)
        queue = self.QUEUES[queue_name] = self.QUEUES.get(queue_name) or []
        return queue

    def _path_params(self, req):
        return req.path_to_match.strip('/').partition('?')[0].split('/')


# ---------------
# UTIL FUNCTIONS
# ---------------

def add_req_params_to_request(req, params):
    path_params = req.get_path_params()
    if isinstance(params, list):
        params = {p: p for p in params}
    values = {}
    for k1, k2 in params.items():
        values[k1] = path_params.get(k2)
        if not values[k1]:
            LOG.info('Unable to extract "%s" from path params: %s' % (values[k1], path_params))
    add_values_to_request(req, values)
    return req


def add_values_to_request(req, values):
    data = req.content()
    for k, v in values.items():
        assign_to_path(data, k, v)
    req.data = json.dumps(data)
    return req
