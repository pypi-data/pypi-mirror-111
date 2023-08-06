import json
import types
import logging
from moto.cognitoidp import models as cognitoidp_models, responses as cognitoidp_responses
from moto.cognitoidp.responses import CognitoIdpResponse
from moto.cognitoidp.exceptions import ResourceNotFoundError, UserNotFoundError
from moto.cognitoidentity.models import cognitoidentity_backends
from moto.cognitoidentity.responses import CognitoIdentityResponse
from localstack import config as localstack_config
from localstack.services import infra as localstack_infra
from localstack.constants import LOCALHOST_HOSTNAME
from localstack.utils.common import short_uid
from localstack_ext.services.base import prepare_and_load_persistence_for_moto_backend
from localstack_ext.services.cognito import cognito_helpers

LOG = logging.getLogger(__name__)

# ports lazily initialized on startup
PORT_COGNITO_IDP_BACKEND = None
PORT_COGNITO_IDENTITY_BACKEND = None


def patch_moto():

    # add missing regions in moto backends
    for region in localstack_config.VALID_REGIONS:
        if region not in cognitoidp_models.cognitoidp_backends:
            cognitoidp_models.cognitoidp_backends[region] = cognitoidp_models.CognitoIdpBackend(region)

    # patch "add_custom_attributes"

    def add_custom_attributes(self):
        pool_id = self._get_param('UserPoolId')
        attributes = self._get_param('CustomAttributes')
        user_pool = cognitoidp_models.cognitoidp_backends[self.region].user_pools.get(pool_id)
        if not user_pool:
            raise ResourceNotFoundError(pool_id)
        cfg = user_pool.extended_config
        schema = cfg.get('SchemaAttributes') or []
        attribute_names = [a['Name'] for a in attributes]
        schema = [a for a in schema if a['Name'] not in attribute_names]
        schema.extend(attributes)
        cfg['SchemaAttributes'] = schema
        return ''

    if not hasattr(CognitoIdpResponse, 'add_custom_attributes'):
        CognitoIdpResponse.add_custom_attributes = add_custom_attributes

    def admin_delete_user_attributes(self):
        pool_id = self._get_param('UserPoolId')
        username = self._get_param('Username')
        attr_names = self._get_param('UserAttributeNames')
        user_pool = cognitoidp_models.cognitoidp_backends[self.region].user_pools.get(pool_id)
        if not user_pool:
            raise ResourceNotFoundError(pool_id)
        result = get_user_pool_user(self, user_pool, username)
        if not result:
            raise UserNotFoundError('%s/%s' % (pool_id, username))
        _, user = result
        user.attributes = [a for a in user.attributes if a['Name'] not in attr_names]
        return ''

    CognitoIdpResponse.admin_delete_user_attributes = admin_delete_user_attributes

    def delete_user_attributes(self):
        access_token = self._get_param('AccessToken')
        attr_names = self._get_param('UserAttributeNames')
        token = cognito_helpers.CognitoRegion.ACCESS_TOKENS.get(access_token)
        pool_id = token['pool_id']
        username = token['username']
        user_pool = cognitoidp_models.cognitoidp_backends[self.region].user_pools.get(pool_id)
        if not user_pool:
            raise ResourceNotFoundError(pool_id)
        result = get_user_pool_user(self, user_pool, username)
        if result:
            _, user = result
            user.attributes = [a for a in user.attributes if a['Name'] not in attr_names]
        return ''

    CognitoIdpResponse.delete_user_attributes = delete_user_attributes

    # patch cognitoidp_backends.keys() to allow direct array access

    class DictWithKeysList(dict):
        def keys(self, *args, **kwargs):
            return list(super(DictWithKeysList, self).keys(*args, **kwargs))

    cognitoidp_models.cognitoidp_backends = DictWithKeysList(cognitoidp_models.cognitoidp_backends)
    cognitoidp_responses.cognitoidp_backends = cognitoidp_models.cognitoidp_backends

    # patch "update_user_pool"

    def update_user_pool(self, *args, **kwargs):
        pool_id = self._get_param('UserPoolId')
        user_pool = cognitoidp_models.cognitoidp_backends[self.region].user_pools[pool_id]
        if not user_pool:
            raise ResourceNotFoundError(pool_id)
        body = json.loads(self.body)
        user_pool.extended_config.update(body)
        return ''

    if not hasattr(CognitoIdpResponse, 'update_user_pool'):
        CognitoIdpResponse.update_user_pool = update_user_pool

    # util method to retrieve user pool users

    def get_user_pool_user(self, user_pool, username):
        result = [(k, v) for k, v in user_pool.users.items() if username == k]
        if result:
            return result[0]
        case_sensitive = user_pool.extended_config.get('UsernameConfiguration', {}).get('CaseSensitive', True)
        if not case_sensitive:
            result = [(k, v) for k, v in user_pool.users.items() if username.lower() == k.lower()]
            if result:
                return result[0]
        # try to determine canonical username as fallback
        try:
            username = cognito_helpers.get_canonical_username(username, pool_id=user_pool.id)
            result = [(k, v) for k, v in user_pool.users.items() if username == k]
            if result:
                return result[0]
        except Exception:
            pass

    # patch "delete_user" to consider CaseInsensitive user names

    def patch_admin_delete_user(backend):
        def admin_delete_user(self, pool_id, username, *args, **kwargs):
            try:
                admin_delete_user_orig(pool_id, username, *args, **kwargs)
            except UserNotFoundError:
                user_pool = self.user_pools.get(pool_id)
                result = get_user_pool_user(self, user_pool, username)
                if result:
                    canonical_name, _ = result
                    return admin_delete_user_orig(pool_id, canonical_name, *args, **kwargs)
                raise
        admin_delete_user_orig = backend.admin_delete_user
        return types.MethodType(admin_delete_user, backend)

    for region, backend in cognitoidp_models.cognitoidp_backends.items():
        backend.admin_delete_user = patch_admin_delete_user(backend)

    def user_pool_init(self, *args, **kwargs):
        user_pool_init_orig(self, *args, **kwargs)
        schema = self.extended_config.get('Schema')
        schema_attrs = self.extended_config.get('SchemaAttributes')
        if schema and not schema_attrs:
            self.extended_config['SchemaAttributes'] = self.extended_config.pop('Schema')

    user_pool_init_orig = cognitoidp_models.CognitoIdpUserPool.__init__
    cognitoidp_models.CognitoIdpUserPool.__init__ = user_pool_init

    # make sure Domain is present as part of user pool response

    def pool_to_json(self, extended=False, *args, **kwargs):
        result = pool_to_json_orig(self, extended=extended, *args, **kwargs)
        if extended and not result.get('Domain'):
            # lookup domain and add to pool details response
            domains = cognitoidp_models.cognitoidp_backends[self.region].user_pool_domains
            domain = [d for d in domains.values() if d.user_pool_id == self.id]
            if domain:
                result['Domain'] = domain[0].domain
        return result

    pool_to_json_orig = cognitoidp_models.CognitoIdpUserPool.to_json
    cognitoidp_models.CognitoIdpUserPool.to_json = pool_to_json

    # patch user pool domain names

    def _distribution_name(self):
        return 'https://%s.auth.%s' % (short_uid(), LOCALHOST_HOSTNAME)

    cognitoidp_models.CognitoIdpUserPoolDomain._distribution_name = _distribution_name

    # patch "list_users"

    def list_users(self, *args, **kwargs):
        user_pool_id = self._get_param('UserPoolId')
        users, token = cognitoidp_models.cognitoidp_backends[self.region].list_users(user_pool_id)
        # temporarily add username attribute
        for user in users:
            user.attributes.append({'Name': 'username', 'Value': user.username})
        result = list_users_orig(self, *args, **kwargs)
        # remove temporarily added attributes
        for user in users:
            del user.attributes[-1]
        return result

    list_users_orig = CognitoIdpResponse.list_users
    CognitoIdpResponse.list_users = list_users

    # patch "list_identity_pools"

    def list_identity_pools(self, *args, **kwargs):
        result = cognitoidentity_backends[self.region].identity_pools.values()
        result = {'IdentityPools': [
            {'IdentityPoolId': pool.identity_pool_id, 'IdentityPoolName': pool.identity_pool_name} for pool in result
        ]}
        return json.dumps(result)

    if not hasattr(CognitoIdentityResponse, 'list_identity_pools'):
        CognitoIdentityResponse.list_identity_pools = list_identity_pools

    # patch "set_identity_pool_roles"

    def set_identity_pool_roles(self, *args, **kwargs):
        pool_id = self._get_param('IdentityPoolId')
        pool = cognitoidentity_backends[self.region].identity_pools[pool_id]
        pool.roles = self._get_param('Roles')
        pool.role_mappings = self._get_param('RoleMappings')
        return ''

    if not hasattr(CognitoIdentityResponse, 'set_identity_pool_roles'):
        CognitoIdentityResponse.set_identity_pool_roles = set_identity_pool_roles

    # patch "delete_identity_pool"

    def delete_identity_pool(self, *args, **kwargs):
        pool_id = self._get_param('IdentityPoolId')
        cognitoidentity_backends[self.region].identity_pools.pop(pool_id)
        return ''

    if not hasattr(CognitoIdentityResponse, 'delete_identity_pool'):
        CognitoIdentityResponse.delete_identity_pool = delete_identity_pool

    # patch CognitoIdpUser constructor

    def user_init(self, *args, **kwargs):
        result = user_init_orig(self, *args, **kwargs)
        # align user id with "sub" attribute
        existing_sub = [a for a in self.attributes if a['Name'] == 'sub']
        if existing_sub:
            # update user id from existing "sub" attribute
            self.id = existing_sub[0]['Value']
        else:
            # add user id as "sub" to attributes
            self.update_attributes([{'Name': 'sub', 'Value': self.id}])
        return result

    user_init_orig = cognitoidp_models.CognitoIdpUser.__init__
    cognitoidp_models.CognitoIdpUser.__init__ = user_init


def start_cognito_identity(port=None, asynchronous=False, update_listener=None):
    global PORT_COGNITO_IDENTITY_BACKEND
    port = port or localstack_config.PORT_COGNITO_IDENTITY
    PORT_COGNITO_IDENTITY_BACKEND = localstack_infra.get_multiserver_or_free_service_port()
    return localstack_infra.start_moto_server('cognito-identity', port=port,
        name='Cognito Identity', backend_port=PORT_COGNITO_IDENTITY_BACKEND,
        asynchronous=asynchronous, update_listener=update_listener)


def start_cognito_idp(port=None, asynchronous=False, update_listener=None):
    global PORT_COGNITO_IDP_BACKEND
    port = port or localstack_config.PORT_COGNITO_IDP
    PORT_COGNITO_IDP_BACKEND = localstack_infra.get_multiserver_or_free_service_port()

    # apply runtime code patches
    patch_moto()
    # initialize persistence mechanism
    cognito_helpers.CognitoRegion.restore_and_setup_persistence('cognito-idp')
    prepare_and_load_persistence_for_moto_backend('cognito-idp', cognitoidp_models.cognitoidp_backends)

    return localstack_infra.start_moto_server('cognito-idp', port=port,
        asynchronous=asynchronous, backend_port=PORT_COGNITO_IDP_BACKEND,
        name='Cognito Identity Provider (IdP)', update_listener=update_listener)
