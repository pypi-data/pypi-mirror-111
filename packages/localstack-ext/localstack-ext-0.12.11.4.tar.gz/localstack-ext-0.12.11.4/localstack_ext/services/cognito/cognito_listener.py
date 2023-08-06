import os
import re
import json
import base64
import logging
import traceback
from jwt import utils as jwt_utils
from localstack import config
from localstack.utils.common import to_str, short_uid, load_file
from localstack.utils.analytics import event_publisher
from localstack.services.generic_proxy import ProxyListener
from localstack.utils.aws.aws_responses import requests_response, ErrorResponse
from localstack_ext.services.cognito import cognito_helpers

LOG = logging.getLogger(__name__)

EVENT_COGNITO_CREATE_POOL = 'cgn.cp'
EVENT_COGNITO_DELETE_POOL = 'cgn.dp'

ACTION_PREFIX_IDP = 'AWSCognitoIdentityProviderService'
ACTION_PREFIX_ID = 'AWSCognitoIdentityService'

# backdoor API to resolve credentials at runtime
ACTION_GET_ID_FOR_CREDS = '_get_identity_for_credentials_'


def decode_base64(data):
    """ Decode base64, padding being optional. """
    # TODO: move to common.py
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data = to_str(data) + '=' * (4 - missing_padding)
    return base64.b64decode(data)


def is_cognito_idp_request(path, headers):
    target = headers.get('x-amz-target', '')
    return target.startswith('AWSCognitoIdentityProviderService') or is_cognito_idp_path(path)


def is_cognito_idp_path(path):
    return is_well_known_resource_path(path) or is_login_form_path(path) or is_oauth_request_path(path)


def is_login_form_path(path):
    return path.split('?')[0] in ['/login', '/signup', '/forgotPassword']


def is_oauth_request_path(path):
    return path.startswith('/oauth2/token')


def is_well_known_resource_path(path):
    return re.match(r'^(/[^/]+)?/\.well\-known/(jwks\.json|jwks_uri|openid-configuration)(\?[a-zA-Z0-9_-]+)?$', path)


def serve_well_known_resource_path(path):
    jwks_path = re.match(r'^(/[^/]+)?/\.well\-known/(jwks\.json|jwks_uri).*', path)
    if jwks_path:
        return get_well_known_jwks(path)
    openid_path = re.match(r'^(/[^/]+)?/\.well\-known/openid-configuration.*', path)
    if openid_path:
        return handle_well_known_openid_request(path)
    LOG.info('Unable to find handler for well-known Cognito resource path: %s' % path)
    return {}


def handle_well_known_openid_request(path):
    base_url = config.get_edge_url()
    result = {}
    parts = path.split('/')
    if len(parts) > 3:
        pool_id = parts[1]
        pool_url = '%s/%s' % (base_url, pool_id)
        result = {
            'authorization_endpoint': '%s/oauth2/authorize' % base_url,
            'id_token_signing_alg_values_supported': ['RS256'],
            'issuer': pool_url,
            'jwks_uri': '%s/.well-known/jwks.json' % pool_url,
            'response_types_supported': ['code', 'token', 'token id_token'],
            'scopes_supported': ['openid', 'email', 'phone', 'profile'],
            'subject_types_supported': ['public'],
            'token_endpoint': '%s/oauth2/token' % base_url,
            'token_endpoint_auth_methods_supported': ['client_secret_basic', 'client_secret_post'],
            'userinfo_endpoint': '%s/oauth2/userInfo' % base_url
        }
    return result


def get_well_known_jwks(path):
    # return /.well-known/jwks_uri
    if len(path.split('/')) <= 3:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'well-known-keys.json')
        result = json.loads(load_file(path))
        return result
    result = []
    pub_key = cognito_helpers.get_test_jwt_keypair()[0]
    entry = {
        'kty': 'RSA',
        'alg': 'RS256',
        'use': 'sig',
        'kid': cognito_helpers.TEST_JWT_KEY_ID,
        'n': to_str(jwt_utils.to_base64url_uint(pub_key.n)),
        'e': to_str(jwt_utils.to_base64url_uint(pub_key.e))
    }
    # small backdoor to include the private key in the response as well
    include_pk = '?full' in path
    if include_pk:
        priv_key = cognito_helpers.get_test_jwt_keypair()[1]
        entry['private_key'] = {
            'n': to_str(jwt_utils.to_base64url_uint(priv_key.n)),
            'e': to_str(jwt_utils.to_base64url_uint(priv_key.e)),
            'd': to_str(jwt_utils.to_base64url_uint(priv_key.d)),
            'p': to_str(jwt_utils.to_base64url_uint(priv_key.p)),
            'q': to_str(jwt_utils.to_base64url_uint(priv_key.q))
        }
    result.append(entry)
    return {'keys': result}


class ProxyListenerCognito(ProxyListener):

    def forward_request(self, method, path, data, headers):

        if method == 'OPTIONS':
            return 200

        if is_well_known_resource_path(path):
            return serve_well_known_resource_path(path)

        # get action header
        action = headers.get('X-Amz-Target', '')
        action = action.split('.')[-1]

        try:
            # special routes
            if is_login_form_path(path):
                if method == 'GET':
                    markup = cognito_helpers.render_login_form(path)
                    return requests_response(markup, headers={'Content-type': 'text/html'})
                elif method == 'POST':
                    return cognito_helpers.login_via_form(path, data)
            if method == 'POST' and is_oauth_request_path(path):
                return cognito_helpers.get_oauth2_token(path, data, headers)

            # parse request data
            data = json.loads(to_str(data or '{}'))

            # regular API routes
            if action == 'CreateUserPool':
                event_publisher.fire_event(EVENT_COGNITO_CREATE_POOL,
                    {'p': event_publisher.get_hash(data.get('PoolName'))})
            elif action == 'SignUp':
                return cognito_helpers.signup_user(data)
            elif action == 'AdminConfirmSignUp':
                return cognito_helpers.admin_confirm_sign_up(data)
            elif action == 'AdminCreateUser':
                return cognito_helpers.admin_create_user(data, headers)
            elif action == 'AdminDeleteUser':
                return cognito_helpers.admin_delete_user(data, headers)
            elif action == 'ConfirmSignUp':
                return cognito_helpers.confirm_signup(data)
            elif action == 'AdminInitiateAuth':
                return cognito_helpers.admin_initiate_auth(data)
            elif action == 'AdminRespondToAuthChallenge':
                return cognito_helpers.admin_respond_to_auth_challenge(data)
            elif action == 'InitiateAuth':
                return cognito_helpers.initiate_auth(data)
            elif action == 'RespondToAuthChallenge':
                return cognito_helpers.respond_to_auth_challenge(data)
            elif action == 'UpdateUserAttributes':
                return cognito_helpers.update_user_attributes(data)
            elif action == 'AdminUpdateUserAttributes':
                return cognito_helpers.admin_update_user_attributes(data, headers)
            elif action == 'GetUser':
                return cognito_helpers.get_user(data)
            elif action == 'GetUserPoolMfaConfig':
                return cognito_helpers.get_user_pool_mfa_config(data)
            elif action == 'SetUserPoolMfaConfig':
                return cognito_helpers.set_user_pool_mfa_config(data)
            elif action == 'SetUserMFAPreference':
                return cognito_helpers.set_user_mfa_preference(data)
            elif action == 'AdminSetUserMFAPreference':
                return cognito_helpers.admin_set_user_mfa_preference(data)
            elif action == 'ForgotPassword':
                return cognito_helpers.forgot_password(data)
            elif action == 'ChangePassword':
                return cognito_helpers.change_password(data)
            elif action == 'ConfirmForgotPassword':
                return cognito_helpers.confirm_forgot_password(data)
            elif action == 'AdminSetUserPassword':
                return cognito_helpers.admin_set_user_password(data)
            elif action == 'GetSigningCertificate':
                return cognito_helpers.get_signing_certificate(data)
            elif action == 'AdminGetUser':
                return cognito_helpers.admin_get_user(data, headers)
            elif action == 'GlobalSignOut':
                return cognito_helpers.global_sign_out(data)
            elif action == 'AdminUserGlobalSignOut':
                return cognito_helpers.admin_user_global_sign_out(data)
        except cognito_helpers.CognitoException as e:
            msg = 'Error in Cognito action "%s": %s %s' % (action, e, traceback.format_exc() if config.DEBUG else '')
            LOG.info(msg)
            return cognito_helpers.error_response(e.message, error_type=e.error_type, code=e.status_code)
        except ErrorResponse as e:
            return e.response
        except Exception as e:
            if 'Unable to find' in str(e) or 'Cannot find' in str(e):
                return cognito_helpers.error_response('Cannot find resource: %s' % e,
                    error_type='ResourceNotFoundException', code=404)
            msg = 'Error in Cognito action "%s": %s %s' % (action, e, traceback.format_exc() if config.DEBUG else '')
            LOG.info(msg)
            return cognito_helpers.error_response(msg, error_type='InternalServerError', code=500)

        return True

    def return_response(self, method, path, data, headers, response):
        if response.status_code >= 400:
            return response
        action = headers.get('X-Amz-Target', '')
        action = action.split('.')[-1]
        try:
            data = json.loads(to_str(data or '{}'))
        except Exception:
            pass

        if action == 'CreateUserPool':
            cognito_helpers.user_pool_created(response)
        elif action == 'CreateUserPoolClient':
            response = cognito_helpers.user_pool_client_created(data, response)
        elif action == 'DescribeUserPoolClient':
            response = cognito_helpers.describe_user_pool_client(data, response)
        elif action in ['AdminDeleteUser', 'DeleteUser']:
            response = cognito_helpers.flush_user_state(data, response)
        cognito_helpers.update_user_details_in_response(headers, response)


class ProxyListenerCognitoIdentity(ProxyListener):

    def forward_request(self, method, path, data, headers):
        action = headers.get('X-Amz-Target', '')
        action = action.split('.')[-1]

        if is_well_known_resource_path(path):
            return serve_well_known_resource_path(path)

        data = json.loads(to_str(data or '{}'))
        if action == ACTION_GET_ID_FOR_CREDS:
            auth = headers.get('Authorization') or ''
            access_id = re.sub(r'.*Credential=([^/]+)/.*', r'\1', auth)
            identity_id = cognito_helpers.CognitoRegion.CREDENTIAL_IDENTITIES.get(access_id)
            if not identity_id:
                return requests_response({'error': 'Unable to verify access ID %s' % access_id}, status_code=404)
            return {'IdentityId': identity_id,
                'UserName': cognito_helpers.CognitoRegion.IDENTITY_USERS.get(identity_id)}
        elif action == 'GetIdentityPoolRoles':
            return cognito_helpers.get_identity_pool_roles(data)
        elif action == 'SetIdentityPoolRoles':
            return cognito_helpers.set_identity_pool_roles(data)

        return True

    def return_response(self, method, path, data, headers, response):
        action = headers.get('X-Amz-Target', '')
        action = action.split('.')[-1]

        if action == 'GetId':
            data = json.loads(to_str(data))
            content = json.loads(to_str(response.content))
            identity_id = content['IdentityId']
            jwt = list(data['Logins'].values())[0]
            claims = jwt.split('.')[1]
            claims = decode_base64(claims)
            claims = json.loads(to_str(claims))
            cognito_helpers.CognitoRegion.IDENTITY_USERS[identity_id] = (
                claims.get('cognito:username') or claims.get('username') or claims['sub'])
        if action == 'GetCredentialsForIdentity':
            data = json.loads(to_str(data))
            content = json.loads(to_str(response.content))
            credentials = content['Credentials']
            credentials['AccessKeyId'] = access_id = 'TEST-%s' % short_uid()
            cognito_helpers.CognitoRegion.CREDENTIAL_IDENTITIES[access_id] = data['IdentityId']
            response._content = json.dumps(content)
            response.headers['Content-Length'] = str(len(response._content))


# instantiate listener
UPDATE_COGNITO = ProxyListenerCognito()
UPDATE_COGNITO_IDENTITY = ProxyListenerCognitoIdentity()
