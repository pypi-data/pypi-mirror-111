import re
import hmac
import json
import base64
import hashlib
import logging
import traceback
import jwt
import rsa
import srp
from random import randint
from binascii import hexlify, unhexlify
from cachetools import TTLCache
from flask import Response
from warrant import aws_srp
from requests.models import Request, Response as RequestsResponse
from moto.core.utils import camelcase_to_underscores
from warrant.aws_srp import hex_to_long, hex_hash, pad_hex
from six.moves.urllib import parse as urlparse
from moto.cognitoidp import models as cognitoidp_models
from localstack import config
from localstack.utils.aws import aws_stack, aws_responses
from localstack.utils.common import (
    to_str, to_bytes, short_uid, long_uid, now_utc, json_safe, clone,
    generate_ssl_cert, parse_request_data, select_attributes)
from localstack_ext.constants import TOKEN_EXPIRY_SECONDS
from localstack_ext.bootstrap import email_utils
from localstack_ext.utils.aws import aws_utils
from localstack_ext.utils.common import MultiKeyDict
from localstack_ext.services.base import RegionBackend
from localstack_ext.services.cognito import cognito_triggers
from localstack_ext.services.cognito.signin_form import SIGNIN_FORM_MARKUP
from localstack_ext.services.cognito.cognito_triggers import call_cognito_trigger

LOG = logging.getLogger(__name__)

# caches client ID -> user pool details
CLIENT_POOL_CACHE = TTLCache(maxsize=100, ttl=30)

# list of recent confirmation codes - used for testing purposes
CONFIRMATION_CODES = []

TEST_JWT_KEY_ID = 'test-key'
TEST_JWT_KEYPAIR = None
TEST_SIGNING_CERT_KEY = None

# activation email templates
ACTIVATION_EMAIL_SUBJECT = 'Your verification code'
ACTIVATION_EMAIL_TEMPLATE = """
Your confirmation code is %s
"""

# Callback URL pattern - TODO make configurable?
CALLBACK_URL_PATTERN = 'https://%s/oauth2/idpresponse'
# Client attributes to be forwarded as query parameters in authorize URLs - TODO make configurable?
IDP_CLIENT_ATTRS = ['client_id', 'authorize_scopes', 'authorize_url']

# marker attribute name to indicate a special internal API call
ATTR_MARKER_INTERNAL_CALL = '_internal_'

ATTR_PREFERRED_USERNAME = 'preferred_username'
ATTR_USERNAME_ATTRS = ['email', 'phone_number', ATTR_PREFERRED_USERNAME]

RESERVED_JWT_ATTRIBUTE_NAMES = ['exp', 'iss', 'sub', 'aud', 'auth_time', 'iat', 'event_id', 'token_use']


class CognitoRegion(RegionBackend):
    # maps OAuth2 codes to details
    AUTH_CODES = {}
    # maps secret blocks to challenge details
    CHALLENGES = {}
    # maps user pool or client ids to their regions
    ENTITY_REGIONS = {}
    # maps access token to token details
    ACCESS_TOKENS = {}
    # maps refresh token to token details
    REFRESH_TOKENS = {}
    # maps client secrets (for OAuth2 flows) to user pool client IDs
    CLIENT_SECRETS = {}
    # maps identity IDs to user names
    IDENTITY_USERS = {}
    # maps credentials (access keys) to identity IDs
    CREDENTIAL_IDENTITIES = {}

    # TODO: create a UserPool class to encapsulate the pool-specific attributes below?
    def __init__(self):
        # maps pool_id -> user_id -> user details
        self.users = {}
        # maps pool_id -> (user_name/aliases) -> password
        self.user_passwords = {}
        # maps pool_id -> user_name -> signup_status (may be empty or non-existent)
        self.signup_confirmations = {}
        # maps pool_id -> MFA configs
        self.mfa_configs = {}
        # maps pool_id -> username -> MFA preferences
        self.mfa_user_preferences = {}

    @staticmethod
    def get_for_pool(pool_id):
        region = get_pool_region(pool_id)
        aws_utils.set_default_region_in_request_context(service='cognito-idp', region=region)
        return CognitoRegion.get(region)

    @classmethod
    def should_persist_state_for_request(cls, method, path, data, headers, *args, **kwargs):
        action = headers.get('X-Amz-Target') or ''
        if action.endswith('InitiateAuth'):
            return False
        return super(CognitoRegion, cls).should_persist_state_for_request(
            method, path, data, headers, *args, **kwargs)


class CognitoIdentityRegion(RegionBackend):
    def __init__(self):
        self.identity_pool_roles = {}


class CognitoException(Exception):
    def __init__(self, message=None, error_type=None, status_code=None):
        super(CognitoException, self).__init__()
        self.message = message or 'Request error'
        self.error_type = error_type or 'ClientRequestError'
        self.status_code = status_code or 400


class UserAliasConflictError(Exception):
    """ Exception that indicates that a user alias conflict has occurred (e.g., alias already in use). """
    def __init__(self, *args, **kwargs):
        super(UserAliasConflictError, self).__init__(*args, **kwargs)


def user_pool_created(response):
    # record pool region, to be able to look it up later
    content = json.loads(to_str(response.content))
    pool_id = content['UserPool']['Id']
    CognitoRegion.ENTITY_REGIONS[pool_id] = aws_stack.get_region()
    region_state = CognitoRegion.get_for_pool(pool_id)
    region_state.users[pool_id] = region_state.users.get(pool_id, {})


def user_pool_client_created(data, response):
    # record pool client region, to be able to look it up later
    content = json.loads(to_str(response.content))
    client_id = content['UserPoolClient']['ClientId']
    CognitoRegion.ENTITY_REGIONS[client_id] = aws_stack.get_region()
    # add ClientSecret, if required
    if data.get('GenerateSecret'):
        client_secret = short_uid()
        CognitoRegion.CLIENT_SECRETS[client_secret] = client_id
        content['UserPoolClient']['ClientSecret'] = client_secret
        update_response_content(response, content)
    return response


def describe_user_pool_client(data, response):
    content = json.loads(to_str(response.content))
    client_id = content['UserPoolClient']['ClientId']
    # add ClientSecret, if required
    secret = [k for k, v in CognitoRegion.CLIENT_SECRETS.items() if v == client_id]
    if secret:
        content['UserPoolClient']['ClientSecret'] = secret[0]
        update_response_content(response, content)
    return response


def admin_initiate_auth(data):
    return initiate_auth(data)


def admin_respond_to_auth_challenge(data):
    challenge_name = data['ChallengeName']
    if challenge_name == 'NEW_PASSWORD_REQUIRED':
        pool_id = data['UserPoolId']
        username = data['ChallengeResponses'].get('USERNAME')
        confirm_details = get_signup_confirmation_status(pool_id, username)
        if not confirm_details:
            return error_response('Unable to find confirmation details for pool "%s", username "%s"' %
                                  (pool_id, username), error_type='InvalidParameterException')
        if not username:
            username = confirm_details.get('Username')
        session = confirm_details.get('Session')
        if session != data.get('Session'):
            return error_response('Invalid session identifier specified.', error_type='InvalidParameterException')
        _set_user_password(pool_id, username, data['ChallengeResponses']['NEW_PASSWORD'])
        new_token = issue_token(username=username, client_id=data['ClientId'], pool_id=pool_id)
        result = {
            'ChallengeName': challenge_name,
            'Session': session,
            'AuthenticationResult': new_token
        }
        return result
    return error_response('Unsupported challenge name "%s"' % challenge_name)


def initiate_auth(data):
    client_id = data.get('ClientId', 'CLIENT_ID_NOT_APPLICABLE')
    user_pool = get_pool_client(client_id)
    pool_id = user_pool['UserPoolId']
    username = data.get('AuthParameters', {}).get('USERNAME')

    # call PreAuthentication cognito trigger
    event = {'userNotFound': False}
    if username:
        try:
            event['request'] = {
                'userAttributes': get_user_attributes(username, pool_id=pool_id),
                'validationData': data.get('ClientMetadata', {}) or {}
            }
        except Exception:
            event['userNotFound'] = True

    call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_PRE_AUTH, payload=event, client_id=client_id)

    auth_flow = data['AuthFlow']
    if auth_flow == 'USER_SRP_AUTH':
        result = initiate_auth_srp(data)
    elif auth_flow == 'REFRESH_TOKEN_AUTH':
        result = initiate_auth_refresh_token(data)
    elif auth_flow == 'USER_PASSWORD_AUTH':
        result = initiate_auth_user_pass(data)
    elif auth_flow == 'ADMIN_USER_PASSWORD_AUTH':
        # TODO: for now, simply reuse the initiate_auth without admin features
        result = initiate_auth_user_pass(data)
    elif auth_flow == 'ADMIN_NO_SRP_AUTH':
        # the ADMIN_NO_SRP_AUTH adminInitiateAuth flow is basically identical to USER_PASSWORD_AUTH initiateAuth
        result = initiate_auth_user_pass(data)
    elif auth_flow == 'CUSTOM_AUTH':
        # call Custom Authentication trigger flow
        result = initiate_auth_custom(data, client_id, pool_id)
    else:
        return error_response('Unknown auth flow: %s' % data['AuthFlow'])

    # call PostAuthentication cognito trigger
    event = {}
    if username and isinstance(result, dict) and result.get('AuthenticationResult'):
        event = {'userName': username, 'request': {
            'userAttributes': get_user_attributes(username, pool_id=pool_id)}}
    call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_POST_AUTH, payload=event, client_id=client_id)

    return result


def initiate_auth_custom(data, client_id, pool_id):
    auth_params = data.get('AuthParameters')
    if '_skip_trigger_' in auth_params:
        # use this backdoor functionality to simplify testing
        return
    username = auth_params.get('USERNAME')

    # step 1: call "define auth" trigger Lambda
    trigger_result = call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_AUTH_DEFINE_CHALL, client_id=client_id)
    if not trigger_result:
        return
    response = trigger_result.get('response', {})

    # check trigger response
    fail = response.get('failAuthentication')
    if fail:
        return error_response('Unable to authenticate via custom Cognito trigger: %s' % trigger_result)
    issue = response.get('issueTokens')
    if issue:
        new_token = issue_token(username=username, client_id=client_id, pool_id=pool_id)
        result = {'AuthenticationResult': new_token}
        return json_safe(result)

    # step 2: call "create auth challenge" trigger Lambda
    event = {'request': {'challengeName': response.get('challengeName')}}
    trigger_result = call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_AUTH_CREATE_CHALL,
        client_id=client_id, payload=event)

    response = (trigger_result or {}).get('response', {})
    response['privateChallengeParameters'] = response.get('privateChallengeParameters') or {}
    challenge = response.get('challengeMetadata')
    params = response.get('publicChallengeParameters')
    session = 'Test-Session-%s' % short_uid()

    result = {
        'ChallengeName': challenge,
        'Session': session,
        'ChallengeParameters': params
    }
    challenge_details = {
        'ClientId': client_id,
        'PoolId': pool_id,
        'details': trigger_result,
        'session_list': [result]
    }
    CognitoRegion.CHALLENGES[session] = challenge_details

    return result


def initiate_auth_refresh_token(data, pool_id=None, client_id=None):
    refresh_token = data
    if isinstance(data, dict):
        refresh_token = data['AuthParameters']['REFRESH_TOKEN']
        pool_id = pool_id or data.get('UserPoolId')
        client_id = client_id or data.get('ClientId')
    # Note: do NOT remove the refresh_token from dict, as each token can be used multiple times
    token = CognitoRegion.REFRESH_TOKENS.get(refresh_token)
    if not token:
        return error_response('Invalid refresh token: %s' % refresh_token, error_type='InvalidTokenException')
    pool_id = pool_id or token.get('pool_id')
    client_id = client_id or token.get('client_id')
    new_token = issue_token(subject=token.get('subject'), username=token.get('username'),
                            client_id=client_id, pool_id=pool_id, flow_type='refresh_token')
    result = {
        'AuthenticationResult': new_token
    }
    return json_safe(result)


def check_username_password(client_id, username, password, pool_id=None, req_data=None):
    """ Checks the given credentials and returns a Response object in case of errors, None otherwise. """
    if not username or not password:
        return error_response('Auth parameters username/password not specified', error_type='InvalidParameterException')

    if not pool_id:
        user_pool = get_pool_client(client_id)
        pool_id = user_pool['UserPoolId']

    correct_password = _get_user_password(pool_id, username)

    if not correct_password:
        # trigger user migration if configured, if user does not yet exist
        req_data = req_data or {}
        result = trigger_user_migration(username, client_id=client_id, password=password,
            validation_data=req_data.get('ClientMetadata', {}))
        if is_response_obj(result):
            return result
        correct_password = _get_user_password(pool_id, username)

    if not correct_password:
        return error_response('Unable to find password config for pool "%s", username "%s"' % (pool_id, username),
                              error_type='InvalidParameterException')
    if password != correct_password:
        return error_response('Invalid password specified', error_type='NotAuthorizedException')


def initiate_auth_user_pass(data):
    auth_params = data.get('AuthParameters', {})
    username = auth_params.get('USERNAME')
    password = auth_params.get('PASSWORD')
    client_id = data.get('ClientId')
    user_pool = get_pool_client(client_id)
    pool_id = user_pool['UserPoolId']

    err_response = check_username_password(client_id, username, password, pool_id=pool_id, req_data=data)
    if err_response is not None:
        return err_response

    # check password reset status
    confirm_details = get_signup_confirmation_status(pool_id, username)
    status = confirm_details.get('Status')
    LOG.debug('Account status for user %s in pool %s: %s' % (username, pool_id, status))
    if status in ['FORCE_CHANGE_PASSWORD', 'RESET_REQUIRED']:
        session = 'Test-Session-%s' % short_uid()
        confirm_details['Session'] = session
        confirm_details['Username'] = confirm_details.get('Username') or username
        new_token = issue_token(username=username, client_id=client_id, pool_id=pool_id, flow_type='new_pass')
        result = {
            'ChallengeName': 'NEW_PASSWORD_REQUIRED',
            'Session': session,
            'ChallengeParameters': {
                'USER_ID_FOR_SRP': username,
                'requiredAttributes': '[]',
                'userAttributes': '{}'
            },
            'AuthenticationResult': new_token
        }
        return result

    new_token = issue_token(username=username, client_id=client_id, pool_id=pool_id)
    # TODO delete old token?
    result = {
        'AuthenticationResult': new_token
    }
    return json_safe(result)


def initiate_auth_srp(data):
    auth_params = data['AuthParameters']
    username = auth_params.get('USERNAME')
    if not username:
        return error_response('Username missing')
    client_id = data.get('ClientId')
    if not client_id:
        return error_response('ClientId missing')

    user = find_user(username, client_id=client_id)
    # trigger user migration if configured, if user does not yet exist
    user = trigger_user_migration(username, user=user, client_id=client_id,
        validation_data=data.get('ClientMetadata', {}))
    if not user:
        return error_response('Unknown user "%s" for client id "%s"' %
                              (username, client_id))

    # get canonical username, to enable login for user pools with case-insensitivity enabled
    canonical_username = get_canonical_username(username, client_id=client_id)

    secret_block = b64_encode(short_uid())
    username_to_hash = get_username_for_hashing(canonical_username, client_id=client_id)

    # See: https://github.com/capless/warrant/blob/master/warrant/aws_srp.py
    k_value = hex_to_long(hex_hash('00' + aws_srp.n_hex + '0' + aws_srp.g_hex))
    bytes_A = unhexlify(pad_hex(auth_params['SRP_A']))
    verifier = srp.Verifier(username=username_to_hash,
                            bytes_s=user['__salt__'], bytes_v=user['__vkey__'], bytes_A=bytes_A, k=k_value,
                            hash_alg=srp.SHA256, ng_type=srp.NG_CUSTOM, n_hex=aws_srp.n_hex, g_hex=aws_srp.g_hex)
    s, B = verifier.get_challenge()

    challenge = {
        'ChallengeName': 'PASSWORD_VERIFIER',
        'ChallengeParameters': {
            'USER_ID_FOR_SRP': canonical_username,
            'SALT': hexlify(s),
            'SRP_B': hexlify(B),
            'SECRET_BLOCK': secret_block,
        }
    }
    CognitoRegion.CHALLENGES[secret_block] = {
        'ClientId': client_id,
        'SRP_A': auth_params['SRP_A'],
        '__verifier__': verifier,
        '__b__': verifier.b,
        'challenge': challenge
    }
    return json_safe(challenge)


def respond_to_auth_challenge(data):
    custom_chall_result = respond_auth_challenge_custom(data)
    if custom_chall_result is not None:
        return custom_chall_result

    challenge_name = data['ChallengeName']
    if challenge_name == 'PASSWORD_VERIFIER':
        return respond_auth_challenge_pw_verifier(data)
    if challenge_name == 'NEW_PASSWORD_REQUIRED':
        return respond_auth_challenge_new_password(data)
    return error_response('Unsupported challenge name "%s"' % challenge_name)


def respond_auth_challenge_new_password(data):
    resp = data['ChallengeResponses']
    new_pass = resp.get('NEW_PASSWORD')
    username = resp.get('USERNAME')
    if not new_pass or not username:
        return error_response('Parameters USERNAME and NEW_PASSWORD required in challenge response')

    session_key = to_str(data.get('Session', ''))
    client_id = to_str(data.get('ClientId'))
    if not session_key or not client_id:
        return error_response('Parameters ClientId and Session required in request')

    user_pool = get_pool_client(client_id)
    pool_id = user_pool['UserPoolId']

    confirm_details = get_signup_confirmation_status(pool_id, username, session_key=session_key)
    # check session key
    if confirm_details.get('Session') != session_key:
        return error_response('Invalid Session or USERNAME specified in the request')

    if not username:
        username = confirm_details.get('Username')

    # update account confirmation status and password
    set_signup_confirmation_status(pool_id, username, 'CONFIRMED')
    _set_user_password(pool_id, username, new_pass)

    token = issue_token(username=username, client_id=data.get('ClientId'), pool_id=pool_id)
    result = {
        'ChallengeName': data['ChallengeName'],
        'AuthenticationResult': token
    }
    return result


def respond_auth_challenge_pw_verifier(data):
    resp = data['ChallengeResponses']
    secret_block = resp['PASSWORD_CLAIM_SECRET_BLOCK']
    challenge_details = CognitoRegion.CHALLENGES.get(secret_block)
    if not challenge_details:
        return error_response('Invalid challenge response (secret block)')
    client_id = challenge_details['ClientId']
    pool = get_pool_client(client_id)
    if not pool:
        return error_response('Invalid challenge response (pool)')
    pool_id = pool['UserPoolId']
    verifier = challenge_details['__verifier__']
    params = challenge_details['challenge']['ChallengeParameters']
    user = find_user(resp['USERNAME'], client_id=client_id)
    if not user:
        return error_response('Invalid challenge response (user)')

    # See: https://github.com/capless/warrant/blob/master/warrant/aws_srp.py
    hkdf = aws_srp.compute_hkdf(bytearray.fromhex(pad_hex(verifier.S)),
                                bytearray.fromhex(pad_hex(aws_srp.long_to_hex(verifier.u))))
    # construct message
    msg = (bytearray(pool_id.split('_')[1], 'utf-8') +
           bytearray(params['USER_ID_FOR_SRP'], 'utf-8') +
           bytearray(base64.b64decode(secret_block)) +
           bytearray(resp['TIMESTAMP'], 'utf-8'))
    hmac_obj = hmac.new(hkdf, msg, digestmod=hashlib.sha256)
    # calculate signature
    signature_string = to_str(base64.standard_b64encode(hmac_obj.digest()))

    provided_signature = to_str(resp['PASSWORD_CLAIM_SIGNATURE'])
    if signature_string != provided_signature:
        LOG.debug('Invalid password claim signature string: %s != %s' % (signature_string, provided_signature))
        return error_response('Incorrect username or password.', error_type='NotAuthorizedException')

    # signature is valid, create token
    token = issue_token(username=resp['USERNAME'], client_id=client_id, pool_id=pool_id)
    result = {
        'AuthenticationResult': token
    }
    return json_safe(result)


def respond_auth_challenge_custom(data):
    session = data.get('Session')
    challenge_details = CognitoRegion.CHALLENGES.get(session)
    if not challenge_details:
        return
    client_id = challenge_details['ClientId']
    pool_id = challenge_details['PoolId']
    session_list = challenge_details['session_list']
    trigger_response = challenge_details['details']['response']

    # call verify challenge
    responses = data.get('ChallengeResponses', {})
    request = {
        'challengeAnswer': responses,
        'privateChallengeParameters': trigger_response['privateChallengeParameters'],
        'session': session_list
    }
    result = call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_AUTH_VERIFY_CHALL,
        client_id=client_id, payload={'request': request}) or {}
    answer_correct = result.get('response', {}).get('answerCorrect')
    if not answer_correct:
        return error_response('Invalid auth challenge response for session %s: %s' % (session, responses))

    # finally, call "define auth challenge" Lambda again
    event = {}
    result = call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_AUTH_DEFINE_CHALL,
        client_id=client_id, payload=event)

    # TODO: how to determine the proper username/subject here!?
    subject = 'testuser'
    token = issue_token(subject=subject, client_id=client_id, pool_id=pool_id)
    result = {'AuthenticationResult': token}
    return result


def send_confirmation_email(data, pool_id, username, is_admin_create=False):
    configs = get_signup_confirmation_status(pool_id, username)
    if configs.get('Status') == 'UNCONFIRMED':
        # avoid sending duplicate confirmation emails
        return

    code = generate_confirmation_code()
    configs['ConfirmationCode'] = code
    configs['Status'] = 'UNCONFIRMED'

    # send out confirmation email, if configured
    LOG.info('Confirmation code for Cognito user %s: %s' % (username, code))
    user_email = get_user_email(data)
    if not user_email:
        LOG.info('Unable to send confirmation message, no email address for user "%s" in pool "%s"' %
                 (username, pool_id))
        return

    message = ACTIVATION_EMAIL_TEMPLATE % code
    subject = ACTIVATION_EMAIL_SUBJECT

    # determine custom activation message, if configured
    event = {'userName': username, 'request': {'codeParameter': code, 'usernameParameter': username}}
    trigger_type = (cognito_triggers.TRIGGER_CUSTOM_ADMIN_CREATE if is_admin_create else
        cognito_triggers.TRIGGER_CUSTOM_SIGNUP)
    result = call_cognito_trigger(pool_id, trigger_type, payload=event)
    if result:
        response = result['response']
        subject, message = response['emailSubject'], response['emailMessage']

    try:
        email_utils.send_email(subject, message, user_email)
    except Exception as e:
        LOG.debug('Unable to send email, please update SMTP configuration: %s' % e)


def update_aliases_for_user(pool_id, username, user_attrs, force=False):
    user_attrs = user_attrs or []
    alias_attrs = list(ATTR_USERNAME_ATTRS)

    # fetch username aliases from pool details
    pool_details = get_user_pool_details(pool_id)
    alias_attrs.extend(pool_details.get('UsernameAttributes', []))

    username_aliases = [a['Value'] for a in user_attrs if a['Name'] in alias_attrs]
    if username_aliases:
        password = _get_user_password(pool_id, username)
        if not password:
            LOG.info('Unable to find password config for username %s, aliases %s' % (username, username_aliases))
            return True
        for alias in username_aliases:
            set_user_id_alias(pool_id, username, alias, force=force)


def update_user_attributes(data, pool_id=None, username=None, is_admin=False):
    attrs = data.get('UserAttributes', [])
    access_token = to_str(data.get('AccessToken') or '')
    token_details = CognitoRegion.ACCESS_TOKENS.get(access_token) or {}
    if not token_details and not is_admin:
        return error_response('Invalid access token specified')

    pool_id = pool_id or token_details.get('pool_id')
    username = username or token_details.get('subject')

    set_pool_user_details(pool_id, username, {'UserAttributes': attrs})
    update_aliases_for_user(pool_id, username, attrs)

    return True


def admin_update_user_attributes(data, headers):
    pool_id = data.get('UserPoolId')
    username = data.get('Username')
    update_user_attributes(data, pool_id=pool_id, username=username, is_admin=True)
    canonical = get_canonical_username(username, pool_id=pool_id)
    if canonical != username:
        # update username in request to avoid UserNotFoundException
        data['Username'] = canonical
        return Request(data=json.dumps(data), headers=headers)
    return True


def signup_user(payload_data):
    data = clone(payload_data)
    username = data['Username']

    # TODO: error handling if pool/client not found
    client_id = data['ClientId']
    user_pool = get_pool_client(client_id)
    pool_id = user_pool['UserPoolId']

    # call PreSignup cognito trigger
    event = get_presignup_trigger_event(data)
    trigger_info = call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_SIGNUP, payload=event, client_id=client_id)
    user_confirmed = bool(trigger_info.get('response', {}).get('autoConfirmUser'))

    # configure signup confirmation code
    if get_signup_confirmation_status(pool_id, username):
        return error_response('This user already exists in the user pool', error_type='UsernameExistsException')

    # check if username uses an invalid format (e.g., email address if user pool has email alias enabled)
    response = check_username_format_error(pool_id, username)
    if response is not None:
        return response

    data['UserPoolId'] = pool_id
    # create backend user in UNCONFIRMED state
    set_pool_user_details(pool_id, username, data, create=True)
    add_user_in_backend(pool_id, username, data, raise_if_exists=False)

    # set salted SRP verification key (run this after add_user_in_backend() above, to use unique user ID/`sub`)
    set_srp_verification_key(data, client_id=data['ClientId'])

    set_signup_confirmation_status(pool_id, username, 'CONFIRMED')
    if not user_confirmed:
        send_confirmation_email(data, pool_id, username)
    else:
        # call PostConfirmation trigger
        event = {'userName': username, 'request': {'userAttributes': get_user_attributes(data)}}
        call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_CONFIRM_SIGNUP, payload=event)

    # cache password to be able to verify it later
    _set_user_password(pool_id, username, data['Password'], user_attrs=data.get('UserAttributes'))

    result = {
        'UserConfirmed': user_confirmed,
        'UserSub': data['sub']
    }
    return result


def check_username_format_error(pool_id, username):
    """ Check if username uses an invalid format (e.g., email address if user pool has email alias enabled) """
    alias_attrs = get_pool_alias_attributes(pool_id)
    msg = 'Username cannot be of {attr} format, since user pool is configured for {attr} alias.'
    if 'email' in alias_attrs and email_utils.is_email_address(username):
        return error_response(msg.format(attr='email'), error_type='InvalidParameterException')
    if 'phone_number' in alias_attrs and is_phone_number(username):
        return error_response(msg.format(attr='phone_number'), error_type='InvalidParameterException')


def get_pool_alias_attributes(pool_id):
    # TODO: add caching for better performance - AliasAttributes are immutable once the pool is created
    pool_details = get_user_pool_details(pool_id)
    alias_attrs = pool_details.get('AliasAttributes', [])
    return alias_attrs


def get_pool_username_attributes(pool_id):
    # TODO: add caching for better performance - UsernameAttributes are immutable once the pool is created
    pool_details = get_user_pool_details(pool_id)
    username_attrs = pool_details.get('UsernameAttributes', [])
    return username_attrs


def set_srp_verification_key(data, client_id=None, pool_id=None):
    """ Set salted verification key, see https://github.com/cocagne/pysrp """
    data = data or {}
    password = data.get('Password') or data.get('TemporaryPassword')
    if data.get('__salt__') or not password:
        return
    username = data['Username']
    username_to_hash = get_username_for_hashing(username, client_id=client_id, pool_id=pool_id)
    salt, vkey = srp.create_salted_verification_key(
        username_to_hash, password, hash_alg=srp.SHA256,
        ng_type=srp.NG_CUSTOM, n_hex=aws_srp.n_hex, g_hex=aws_srp.g_hex)
    result = {'__salt__': salt, '__vkey__': vkey}
    data.update(result)
    return result


def set_user_pool_mfa_config(data):
    result = {}
    pool_id = data['UserPoolId']
    region_state = CognitoRegion.get_for_pool(pool_id)
    region_state.mfa_configs[pool_id] = data
    return result


def get_user_pool_mfa_config(data):
    pool_id = data['UserPoolId']
    region_state = CognitoRegion.get_for_pool(pool_id)
    default = {
        'MfaConfiguration': 'OFF',
        'SmsMfaConfiguration': {},
        'SoftwareTokenMfaConfiguration': {}
    }
    result = region_state.mfa_configs.get(pool_id) or default
    result = clone(result)
    not result.get('SmsMfaConfiguration') and result.pop('SmsMfaConfiguration')
    not result.get('SoftwareTokenMfaConfiguration') and result.pop('SoftwareTokenMfaConfiguration')
    return result


def set_user_mfa_preference(data):
    access_token = data.get('AccessToken')
    token_details = CognitoRegion.ACCESS_TOKENS.get(access_token)
    if not token_details:
        return error_response('Invalid access token specified')
    username = token_details['username']
    pool_id = token_details['pool_id']
    result = admin_set_user_mfa_preference(data, pool_id, username)
    return result


def admin_set_user_mfa_preference(data, pool_id=None, username=None):
    pool_id = pool_id or data.get('UserPoolId')
    region_state = CognitoRegion.get_for_pool(pool_id)
    username = username or data.get('Username')
    pool_prefs = region_state.mfa_user_preferences[pool_id] = region_state.mfa_user_preferences.get(pool_id, {})
    pool_prefs[username] = data
    return {}


def change_password(data):
    old_pass = data.get('PreviousPassword')
    new_pass = data.get('ProposedPassword')
    access_token = data.get('AccessToken')
    if not all([old_pass, new_pass, access_token]):
        return error_response('Please specify attributes: PreviousPassword, ProposedPassword, AccessToken')

    access_token = to_str(access_token)
    token_details = CognitoRegion.ACCESS_TOKENS.get(access_token)
    if not token_details:
        return error_response('Invalid access token specified')

    username = token_details['username']
    pool_id = token_details['pool_id']
    existing_password = _get_user_password(pool_id, username)

    if existing_password != old_pass:
        return error_response('Invalid PreviousPassword', 403)

    _set_user_password(pool_id, username, new_pass)

    return {}


def forgot_password(data):
    client_id = data['ClientId']
    user_pool = get_pool_client(client_id)
    pool_id = user_pool['UserPoolId']
    username = data['Username']
    client = connect_for_entity_id('cognito-idp', pool_id)

    # trigger use migration if configured, if user does not yet exist
    user = find_user(username, client_id=client_id)
    user = trigger_user_migration(username, user=user, client_id=client_id,
        client_metadata=data.get('ClientMetadata', {}))

    user = client.admin_get_user(UserPoolId=pool_id, Username=username)
    user_email = get_user_email(user)

    # configure signup confirmation code
    code = generate_confirmation_code()
    status = {
        'Status': 'PASSWORD_RESET',
        'ConfirmationCode': code
    }
    set_signup_confirmation_status(pool_id, username, status)

    message = ACTIVATION_EMAIL_TEMPLATE % code
    subject = ACTIVATION_EMAIL_SUBJECT

    # determine custom activation message, if configured
    event = {'userName': username, 'request': {'codeParameter': code, 'usernameParameter': username}}
    result = call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_CUSTOM_FORGOT, payload=event)
    if result:
        response = result['response']
        subject, message = response['emailSubject'], response['emailMessage']

    LOG.info('Forgot password code for Cognito user %s: %s' % (username, code))
    email_utils.send_email(subject, message, user_email)
    result = {
        'CodeDeliveryDetails': {
            'Destination': user_email,
            'DeliveryMedium': 'EMAIL'
        }
    }
    return result


def confirm_forgot_password(data):
    user_pool = get_pool_client(data['ClientId'])
    pool_id = user_pool['UserPoolId']
    username = data['Username']
    details = get_signup_confirmation_status(pool_id, username)
    if not details:
        return error_response('Cannot find password confirmation for user', error_type='ResourceNotFoundException')
    expected_code = details['ConfirmationCode']
    if data['ConfirmationCode'] != expected_code:
        return error_response('Invalid confirmation code.', error_type='CodeMismatchException')
    details['Status'] = 'CONFIRMED'
    # cache password to be able to verify it later
    _set_user_password(pool_id, username, data['Password'])

    # call PostConfirmation cognito trigger
    event = {'userName': username}
    call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_CONFIRM_FORGOT_PW,
                         payload=event, client_id=data['ClientId'])

    return {}


def admin_set_user_password(data):
    pool_id = data['UserPoolId']
    username = data['Username']
    _set_user_password(pool_id, username, data['Password'], data.get('UserAttributes'))
    set_signup_confirmation_status(pool_id, username, 'CONFIRMED')
    return {}


def _get_user_password(pool_id, username):
    region_state = CognitoRegion.get_for_pool(pool_id)
    region_state.user_passwords[pool_id] = pool_pwds = region_state.user_passwords.get(pool_id, MultiKeyDict())
    result = lookup_entry_considering_case_insensitivity(pool_id, pool_pwds, username)
    return result


def _set_user_password(pool_id, username, password, user_attrs=None):
    region_state = CognitoRegion.get_for_pool(pool_id)
    region_state.user_passwords[pool_id] = pool_pwds = region_state.user_passwords.get(pool_id, MultiKeyDict())
    pool_pwds[username] = password


def trigger_user_migration(username, user=None, client_id=None, password=None,
        client_metadata={}, validation_data={}):
    """ Trigger use migration if configured for the given user pool. """
    if user:
        return user
    user_pool = get_pool_client(client_id)
    pool_id = user_pool['UserPoolId']

    # run migration lambda
    event = {'userName': username, 'request': {'username': username, 'password': password,
        'clientMetadata': client_metadata, 'validationData': validation_data}}
    result = None
    try:
        result = call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_MIGRATE_AUTH,
                                      payload=event, client_id=client_id)
    except Exception:
        return error_response('Unable to run user migration Lambda for user "%s"' % username,
            code=403, error_type='InvalidLambdaResponseException')
    if is_response_obj(result):
        return result
    if not result:
        return user
    response = result.get('response', {})
    status = response.get('finalUserStatus')
    status = status or 'CONFIRMED'
    if status not in ['CONFIRMED', 'RESET_REQUIRED']:
        LOG.info('Expected user migration status CONFIRMED/RESET_REQUIRED, but found: %s' % status)
        return user

    # create user attributes
    attributes = response.get('userAttributes', {})
    attributes = [{'Name': k, 'Value': v} for k, v in attributes.items()]
    details = {'UserAttributes': attributes, 'sub': username}

    # fix username
    result = check_username_format_error(pool_id, username)
    user_sub_updated = None
    username_orig = username
    if result is not None:
        details['sub'] = user_sub_updated = long_uid()
        attributes.append({'Name': 'sub', 'Value': user_sub_updated})
        update_user_attrs_for_aliases(pool_id, username, details)
        username = user_sub_updated

    # create new user
    add_user_in_backend(pool_id, username, details)
    _set_user_password(pool_id, username, password)
    set_signup_confirmation_status(pool_id, username, status)

    # set alias
    if user_sub_updated:
        set_user_id_alias(pool_id, username, username_orig)

    if status == 'RESET_REQUIRED':
        return error_response('Password reset is required', error_type='PasswordResetRequiredException')

    user = find_user(username, client_id)
    return user


def get_oauth2_token(path, data, headers):
    # get request details
    req_data = get_request_from_body_or_query_params(path, data, expected_param='grant_type')

    grant_type = req_data.get('grant_type')
    scopes = [s for s in (req_data.get('scope') or '').split(' ') if s]
    token = None
    if grant_type == 'authorization_code':
        code = req_data.get('code')
        details = CognitoRegion.AUTH_CODES.get(code)
        if not details:
            return error_response('Invalid auth code specified')
        # TODO check code expiry?
        for attr in ['client_id', 'redirect_uri']:
            value = req_data.get(attr)
            if details.get(attr) != value:
                return error_response('Invalid %s specified' % attr)
        token = issue_token(username=details['username'], client_id=details['client_id'], scopes=scopes)
    elif grant_type == 'client_credentials':
        auth_header = headers.get('Authorization', '')
        auth_token = auth_header.split('Basic')[-1].strip()
        if not auth_token:
            return error_response('Missing Authorization header')
        auth_token = to_str(base64.b64decode(auth_token))
        parts = auth_token.split(':')
        client_id = parts[0]
        client_secret = parts[-1]
        matching_client_id = CognitoRegion.CLIENT_SECRETS.get(client_secret)
        if not matching_client_id or matching_client_id != client_id:
            return error_response('Invalid token specified in Authorization header')
        token = issue_token(subject=client_id, client_id=client_id, scopes=scopes)
    elif grant_type == 'refresh_token':
        refresh_token = req_data.get('refresh_token')
        token = initiate_auth_refresh_token(refresh_token)
        if is_response_obj(token):
            return token
        token = token['AuthenticationResult']
    if token:
        for attr in list(token.keys()):
            attr_lower = camelcase_to_underscores(attr).lower()
            token[attr_lower] = token.pop(attr)
        return token
    return error_response('Unsupported grant_type attribute: %s' % grant_type)


def login_via_form(path, data):
    """ Process the form data sent from the Cognito login form with username/password fields. """
    parsed_path = urlparse.urlparse(path)
    query_params = parse_query_string(parsed_path.query)

    redirect_uri = query_params.get('redirect_uri')
    client_id = query_params.get('client_id')
    response_type = query_params.get('response_type')

    headers = {}
    req_data = parse_query_string(data)

    username = req_data.get('username')
    password = req_data.get('password')

    err_response = check_username_password(client_id, username, password)
    if err_response is not None:
        return err_response

    if response_type == 'code':
        code = generate_confirmation_code()
        entry = clone(query_params)
        entry['code'] = code
        entry['data'] = data
        entry['username'] = username
        CognitoRegion.AUTH_CODES[code] = entry
        redirect_params = 'code=%s' % code
    elif response_type == 'token':
        id_token = issue_token(username=username, client_id=client_id)['IdToken']
        redirect_params = 'id_token={t}#id_token={t}'.format(t=id_token)
    else:
        return error_response('Invalid response_type specified in query parameters')
    redirect_uri = '%s%s%s' % (redirect_uri, '&' if '?' in redirect_uri else '?', redirect_params)
    headers['Location'] = redirect_uri
    return aws_responses.requests_response('', headers=headers)


def admin_confirm_sign_up(data):
    # TODO check if admin!
    pool_id = data['UserPoolId']
    username = data['Username']
    confirmation_status = get_signup_confirmation_status(pool_id, username)
    if not confirmation_status:
        return error_response('Unable to find signup confirmation for user %s in pool %s' % (username, pool_id),
                              error_type='InvalidParameterException')
    current_status = confirmation_status['Status']
    if current_status == 'CONFIRMED':
        return error_response('User %s cannot be confirmed. Current status is %s' % (username, current_status),
                              error_type='NotAuthorizedException')
    set_signup_confirmation_status(pool_id, username, 'CONFIRMED')

    # call PostConfirmation cognito trigger
    event = {'userName': username, 'request': {'userAttributes': get_user_attributes(username, pool_id=pool_id)}}
    call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_CONFIRM_SIGNUP, payload=event)

    return 200


def confirm_signup(data):
    user_pool = get_pool_client(data['ClientId'])
    if not user_pool:
        return error_response('Invalid ClientId specified.', error_type='InvalidParameterException')
    pool_id = user_pool['UserPoolId']
    username = data['Username']
    code = data['ConfirmationCode']
    configs = get_signup_confirmation_status(pool_id, username)
    expected_code = configs['ConfirmationCode']
    if code != expected_code:
        return error_response('Invalid confirmation code.', error_type='CodeMismatchException')
    configs['Status'] = 'CONFIRMED'
    add_user_in_backend(pool_id, username, raise_if_exists=False)

    # call PostConfirmation cognito trigger
    event = {'userName': username, 'request': {'userAttributes': get_user_attributes(username, pool_id=pool_id)}}
    call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_CONFIRM_SIGNUP,
                         payload=event, client_id=data['ClientId'])

    return {}


def admin_create_user(data, headers):
    # TODO implement password checks. See real AWS:
    # An error occurred (InvalidPasswordException) when calling the AdminCreateUser operation:
    #    Password did not conform with password policy: Password must have numeric characters

    data_orig = clone(data)
    attrs = data.get('UserAttributes', [])
    is_internal_call = bool([attr for attr in attrs if attr['Name'] == ATTR_MARKER_INTERNAL_CALL])
    data['UserAttributes'] = [attr for attr in attrs if attr['Name'] != ATTR_MARKER_INTERNAL_CALL]
    pool_id = data['UserPoolId']
    username_provided = data['Username']
    user_confirmed = None
    region_state = CognitoRegion.get_for_pool(pool_id)

    if not is_internal_call:
        ensure_sub_in_user(data)

    if region_state.users.get(pool_id):
        user_sub = get_user_sub_from_username_alias(pool_id, username_provided)
        if user_sub and user_sub != username_provided:
            return error_response('An account with the given username already exists.',
                                  code=400, error_type='UsernameExistsException')

    # call PreSignup cognito trigger
    if not is_internal_call:
        event = get_presignup_trigger_event(data)
        trigger_info = call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_ADMIN_CREATE_USER, payload=event)
        user_confirmed = bool(trigger_info.get('response', {}).get('autoConfirmUser', True))

    # determine whether the username is an email/phone alias, then update user attributes
    update_user_attrs_for_aliases(pool_id, username_provided, data)
    username = data['Username']

    # set user details and tmp password
    data_copy = dict(data)
    set_pool_user_details(pool_id, username, data_copy, create=True)
    temporary_pwd = data.get('TemporaryPassword')
    new_password = temporary_pwd or _get_user_password(pool_id, username)
    user_attrs = data.get('UserAttributes')
    if not new_password and not is_internal_call:
        new_password = temporary_pwd = data_copy['TemporaryPassword'] = short_uid()
        LOG.info('Generated temporary password for username "%s": %s' % (username, new_password))
    _set_user_password(pool_id, username, new_password, user_attrs=user_attrs)

    # set salted SRP verification key (make sure to run this after tmp password was generated!)
    key_data = set_srp_verification_key(data_copy, pool_id=pool_id)
    set_pool_user_details(pool_id, username, key_data)

    # initialize confirmation status
    get_signup_confirmation_status(pool_id, username)

    if not is_internal_call:
        if not user_confirmed:
            send_confirmation_email(data, pool_id, username, is_admin_create=True)
        else:
            # call PostConfirmation trigger
            event = {'userName': username}
            call_cognito_trigger(pool_id, cognito_triggers.TRIGGER_CONFIRM_SIGNUP, payload=event)

    if is_internal_call:
        # this is required to fix the confirmation status for regular signups (with non-temporary password)
        set_signup_confirmation_status(pool_id, username, 'UNCONFIRMED')
    if (is_internal_call or user_confirmed) and temporary_pwd:
        # set initial status to FORCE_CHANGE_PASSWORD
        set_signup_confirmation_status(pool_id, username, 'FORCE_CHANGE_PASSWORD')

    # update user alias configs
    try:
        update_aliases_for_user(pool_id, username, user_attrs, force=data.get('ForceAliasCreation'))
    except UserAliasConflictError:
        attr_keys = [attr['Name'] for attr in data.get('UserAttributes', [])]
        attr_type = ('email' if 'email' in attr_keys else
            'phone_number' if 'phone_number' in attr_keys else 'alias')
        msg = 'An account with the %s already exists' % attr_type
        return error_response(msg, code=400, error_type='UsernameExistsException')

    attrs_changed = data_orig.get('UserAttributes', []) != data.get('UserAttributes', [])
    if attrs_changed or data_orig['Username'] != data['Username']:
        return Request(data=json.dumps(data), headers=headers)
    return True


def get_signing_certificate(data):
    global TEST_SIGNING_CERT_KEY
    if not TEST_SIGNING_CERT_KEY:
        cert = generate_ssl_cert(return_content=True)
        cert = re.sub(r'[-]+(BEGIN|END) (CERTIFICATE|PRIVATE KEY)[-]+', '', cert).strip()
        parts = cert.split('\n\n')
        TEST_SIGNING_CERT_KEY = (parts[1].strip().replace('\n', ''), parts[0].strip().replace('\n', ''))
    result = {'Certificate': TEST_SIGNING_CERT_KEY[0]}
    return result


def get_identity_pool_roles(data):
    region = CognitoIdentityRegion.get()
    pool_id = data.get('IdentityPoolId')
    roles = region.identity_pool_roles.get(pool_id)
    if not roles:
        return error_response('Unable to find roles for identity pool "%s"' % pool_id,
                              code=404, error_type='ResourceNotFoundException')
    return roles


def set_identity_pool_roles(data):
    region = CognitoIdentityRegion.get()
    pool_id = data.get('IdentityPoolId')
    region.identity_pool_roles[pool_id] = data
    return {}


def admin_user_global_sign_out(data):
    pool_id = data.get('UserPoolId')
    username = data.get('Username')
    alias = get_user_sub_from_username_alias(pool_id, username)
    cleanup_access_and_refresh_tokens(username=username, pool_id=pool_id, alias=alias)
    return {}


def global_sign_out(data):
    access_token = data.get('AccessToken')
    CognitoRegion.ACCESS_TOKENS.pop(access_token, None)
    cleanup_access_and_refresh_tokens(access_token=access_token)
    return {}


# ---------------
# HELPER METHODS
# ---------------

def render_login_form(path):
    req_params = parse_request_data('GET', path)
    client_id = req_params.get('client_id', '')
    cognito = aws_stack.connect_to_service('cognito-idp')
    try:
        pool = get_pool_for_client(client_id)
    except Exception:
        pool = None
    callback_url = ''
    idp_providers = []
    if not pool:
        LOG.info('Unable to find user pool for client ID %s' % client_id)
    else:
        pool_id = pool['Id']
        pool = cognito.describe_user_pool(UserPoolId=pool_id)['UserPool']
        domain = pool.get('Domain') or 'localhost'
        domain_with_port = '%s:%s' % (domain, config.EDGE_PORT)
        callback_url = CALLBACK_URL_PATTERN % domain_with_port
        providers = cognito.list_identity_providers(UserPoolId=pool_id).get('Providers', [])
        for provider in providers:
            prov_name = provider.get('ProviderName')
            prov_type = provider.get('ProviderType')
            details = cognito.describe_identity_provider(UserPoolId=pool_id, ProviderName=prov_name)
            details = details.get('IdentityProvider', {})
            prov_details = select_attributes(details.get('ProviderDetails', {}), IDP_CLIENT_ATTRS)
            idp_providers.append({'name': prov_name, 'type': prov_type, 'details': prov_details})
    markup = SIGNIN_FORM_MARKUP.replace('%CALLBACK_URL%', callback_url)
    markup = markup.replace('%IDP_PROVIDERS%', json.dumps(idp_providers))
    return markup


def cleanup_access_and_refresh_tokens(access_token=None, username=None, alias=None, pool_id=None):
    def _matches(token, details):
        linked_access_token = details.get('details', {}).get('AccessToken')
        if token in [access_token, linked_access_token]:
            return True
        return details['pool_id'] == pool_id and details['username'] in [username, alias]

    for token_map in [CognitoRegion.ACCESS_TOKENS, CognitoRegion.REFRESH_TOKENS]:
        for token, details in dict(token_map).items():
            if _matches(token, details):
                token_map.pop(token)


def get_signup_confirmation_status(pool_id, user_id, create_entry=False, session_key=None):
    region = CognitoRegion.get_for_pool(pool_id)
    region.signup_confirmations[pool_id] = configs = region.signup_confirmations.get(pool_id) or MultiKeyDict()
    result = lookup_entry_considering_case_insensitivity(pool_id, configs, user_id) or {}
    if not user_id and session_key:
        tmp = [(k, v) for k, v in configs.items() if v.get('Session') == session_key]
        if tmp:
            user_id, result = tmp[0]
    if create_entry and user_id not in configs:
        configs[user_id] = result
    return result


def set_signup_confirmation_status(pool_id, user_id, status):
    region_state = CognitoRegion.get_for_pool(pool_id)
    get_signup_confirmation_status(pool_id, user_id, create_entry=True)
    status = status if isinstance(status, dict) else {'Status': status}
    region_state.signup_confirmations[pool_id][user_id].update(status)


def get_presignup_trigger_event(data):
    username = data['Username']
    client_id = data.get('ClientId')
    user_attrs = get_user_attributes(data)
    user_attrs.update({'username': username, 'client_id': client_id})
    request = {'userAttributes': user_attrs}
    event = {'request': request}
    return event


def get_user_email(user, pool_id=None):
    return get_user_attributes(user, 'email', pool_id=pool_id)['email']


def get_user_attributes(user, attributes=None, pool_id=None):
    if attributes:
        attributes = attributes if isinstance(attributes, list) else [attributes]
    if isinstance(user, dict):
        user_details = user
    else:
        user_details = get_user_for_username_alias(pool_id, user)
    result = {}
    user_attributes = user_details.get('UserAttributes', [])
    user_attributes = dict([(a['Name'], a['Value']) for a in user_attributes])
    attributes = attributes or list(user_attributes.keys())
    for attr in attributes:
        result[attr] = user_attributes.get(attr)
    return result


def get_user_for_username_alias(pool_id, username):
    region_state = CognitoRegion.get_for_pool(pool_id)
    client = connect_for_entity_id('cognito-idp', pool_id)
    aliases = []
    _get_user_password(pool_id, username)
    passwords_dict = region_state.user_passwords[pool_id]
    case_insensitive = is_case_insensitive_pool(pool_id)

    for key in passwords_dict.keys():
        contained = username in key.values
        if not contained and case_insensitive:
            contained = [v for v in key.values if str(v).lower() == str(username).lower()]
        if contained:
            for alias in key.values:
                if alias not in aliases:
                    aliases.append(alias)
    # TODO: make this approach more efficient! - this is a performance killer currently!
    for alias in aliases:
        try:
            user_details = client.admin_get_user(UserPoolId=pool_id, Username=alias)
            user_attrs = user_details['UserAttributes'] = user_details.get('UserAttributes', [])
            user_attrs_map = dict([(a['Name'], a['Value']) for a in user_attrs])
            if 'cognito:username' not in user_attrs_map:
                user_attrs.append({'Name': 'cognito:username', 'Value': alias})
            return user_details
        except Exception:
            pass
    LOG.debug('Unable to find user object for username alias "%s"' % username)
    raise CognitoException(message='User does not exist.', error_type='UserNotFoundException')


def set_user_id_alias(pool_id, user_id1, user_id2, force=False):
    region_state = CognitoRegion.get_for_pool(pool_id)
    config = region_state.signup_confirmations[pool_id] = region_state.signup_confirmations.get(pool_id, MultiKeyDict())
    pwd_config = region_state.user_passwords[pool_id] = region_state.user_passwords.get(pool_id, MultiKeyDict())
    try:
        pwd_config.set_alias(user_id1, user_id2, force_remap=force)
    except MultiKeyDict.AliasValueConflict as e:
        raise UserAliasConflictError(e)
    config.set_alias(user_id1, user_id2, force_remap=force)


def get_user_sub_from_username_alias(user_pool_id, user_alias, get_username=False):
    """ When username alias (e.g., email, phone) is used to retreive the user information and sub
        is used as user name, this function is used to get the sub from the alias. """

    region_state = CognitoRegion.get_for_pool(user_pool_id)
    case_insensitive = is_case_insensitive_pool(user_pool_id)

    def alias_matches(user_alias, expected_alias):
        if case_insensitive:
            user_alias, expected_alias = user_alias.lower(), expected_alias.lower()
        return user_alias == expected_alias

    pool_users = region_state.users.get(user_pool_id, {})
    for user_name, details in pool_users.items():
        user_sub = details.get('sub')
        if user_sub == user_alias:
            return user_sub
        for attribute in details.get('UserAttributes') or []:
            if attribute.get('Name') in ATTR_USERNAME_ATTRS and alias_matches(attribute.get('Value'), user_alias):
                if get_username:
                    return details.get('Username')
                return user_sub


def admin_delete_user(data, headers):
    pool_id = data['UserPoolId']
    region_state = CognitoRegion.get_for_pool(pool_id)
    result = resolve_alias_in_admin_user_request(data, headers)
    username = data.get('Username')
    region_state.signup_confirmations.get(pool_id, {}).pop(username, None)
    region_state.user_passwords.get(pool_id, {}).pop(username, None)
    return result


def admin_get_user(data, headers):
    return resolve_alias_in_admin_user_request(data, headers)


def flush_user_state(data, response):
    pool_id = data.get('UserPoolId')
    username = data.get('Username')
    if not pool_id:
        access_token = data.get('AccessToken')
        details = CognitoRegion.ACCESS_TOKENS.pop(access_token, {})
        pool_id = details.get('pool_id')
        username = details.get('username')
    if not pool_id or not username:
        LOG.info('Unable to find username or user pool when trying to flush user state: %s' % data)
        return
    region_state = CognitoRegion.get_for_pool(pool_id)
    pool_users = region_state.users.get(pool_id, {})
    pool_users.pop(username, None)
    user_sub = get_user_sub_from_username_alias(pool_id, username)
    if user_sub:
        pool_users.pop(user_sub, None)


def resolve_alias_in_admin_user_request(data, headers=None):
    """ Inspect the given request and resolve any username aliases, before the request gets forwarded. """

    pool_id = data.get('UserPoolId')
    region_state = CognitoRegion.get_for_pool(pool_id)
    if pool_id not in region_state.users:
        raise Exception('Unable to find user pool %s' % pool_id)

    # if username alias is provided (and user pool is configured with username attrs.), then use "sub" for username
    alias_attrs = get_pool_username_attributes(pool_id)
    alias_attrs += get_pool_alias_attributes(pool_id)
    if alias_attrs:
        user_sub = get_user_sub_from_username_alias(pool_id, data['Username'], get_username=True)
        if user_sub:
            data['Username'] = user_sub

    return Request(data=json.dumps(data), headers=headers)


def get_user(data):
    access_token = data.get('AccessToken') or ''
    details = CognitoRegion.ACCESS_TOKENS.get(access_token)
    if not details:
        return error_response('Unable to find user details for the given AccessToken',
                              code=404, error_type='InvalidTokenException')
    username = details['username']
    pool_id = details['pool_id']

    username = get_canonical_username(username, pool_id=pool_id)
    pool_region = get_pool_region(pool_id)
    cognito = aws_stack.connect_to_service('cognito-idp', region_name=pool_region)
    # TODO: return CognitoRegion.users entry directly here, instead of calling backend here
    result = cognito.admin_get_user(UserPoolId=pool_id, Username=username)
    return result


def set_pool_user_details(pool_id, username, data, create=False):
    region_state = CognitoRegion.get_for_pool(pool_id)
    region_state.users[pool_id] = region_state.users.get(pool_id, {})
    data = data or {}
    existing = region_state.users[pool_id].get(username)

    if not existing and not create:
        username = get_canonical_username(username, pool_id=pool_id)
        existing = region_state.users[pool_id].get(username)

    if existing:
        data = dict(data)
        for attr in ['UserPoolId', 'ClientId', 'Username']:
            new_attr = data.get(attr)
            old_attr = existing.get(attr)
            if attr in data and attr in existing and new_attr != old_attr:
                LOG.info('Skip overwriting attribute %s (from "%s" to "%s") for user %s, pool %s' %
                    (attr, old_attr, new_attr, username, pool_id))
                data.pop(attr)

        # Note: here we are only adding/updating attributes, not deleting existing ones
        ex_attrs = existing.get('UserAttributes') or []
        for attr in data.pop('UserAttributes', []):
            ex_attrs = [a for a in ex_attrs if a['Name'] != attr['Name']]
            ex_attrs.append(attr)
        existing['UserAttributes'] = ex_attrs

        # update remaining user details
        existing.update(data)
    elif create:
        region_state.users[pool_id][username] = data


def update_response_content(response, content):
    response._content = json.dumps(content)
    response.headers['Content-Length'] = str(len(response._content))


def get_sub_from_user_attrs(user, only_attrs=False):
    attrs = user.get('UserAttributes', [])
    attrs.extend(user.get('Attributes', []))
    existing = [a for a in attrs if a['Name'] == 'sub']
    if existing:
        return existing[0]['Value']
    if not only_attrs:
        user.get('sub')


def get_combined_distinct_attributes(user):
    result = {}
    for attr_name in ['UserAttributes', 'Attributes']:
        for attr in user.get(attr_name, []):
            result[attr['Name']] = attr['Value']
    return [{'Name': k, 'Value': v} for k, v in result.items()]


def update_user_details_in_response(headers, response):
    """ Patch UserStatus and other attributes we receive from moto. """
    try:
        content = json.loads(to_str(response.content))
    except Exception:
        return

    def fix_user_status(user):
        updated = False
        pool_id = user.get('UserPoolId')
        username = user.get('Username')
        status = (get_signup_confirmation_status(pool_id, username) or {}).get('Status')
        if status:
            user['UserStatus'] = status
            updated = True
        attrs_before = get_combined_distinct_attributes(user)
        # remove internal marker attributes
        attrs_after = [a for a in attrs_before if a['Name'] != ATTR_MARKER_INTERNAL_CALL]
        # note: Cognito returns UserAttributes for "get_user" and Attributes for "list_user"
        # operations - for now we simply return both, but in the future we may want to fix the logic
        user['UserAttributes'] = attrs_after
        user['Attributes'] = attrs_after
        updated = updated or len(attrs_before) != len(attrs_after)
        return updated

    updated = False
    if 'Users' in content:
        for user in content['Users']:
            updated = fix_user_status(user) or updated
    if 'User' in content:
        updated = fix_user_status(content['User']) or updated

    action = headers.get('X-Amz-Target', '').split('.')[-1]
    if action == 'AdminGetUser':
        updated = fix_user_status(content) or updated

    if not updated:
        return

    update_response_content(response, content)
    return response


def connect_for_entity_id(service_name, entity_id):
    region = CognitoRegion.ENTITY_REGIONS.get(entity_id)
    if not region:
        LOG.warning('Unable to determine region for user pool or pool client %s' % entity_id)
    return aws_stack.connect_to_service(service_name, region_name=region)


def generate_confirmation_code():
    # 6 digits numerical code, as in AWS
    code = str(randint(100000, 999999))
    CONFIRMATION_CODES.append(code)
    max_entries = 50
    while len(CONFIRMATION_CODES) > max_entries:
        del CONFIRMATION_CODES[0]
    return code


def ensure_sub_in_user(user):
    user_sub = user.get('sub') or get_sub_from_user_attrs(user) or long_uid()
    user_attrs = user['UserAttributes'] = user.get('UserAttributes', [])
    user['sub'] = user_sub
    sub_attr = get_sub_from_user_attrs(user, only_attrs=True)
    if not sub_attr:
        # add existing sub to attributes
        user_attrs.append({'Name': 'sub', 'Value': user_sub})


def add_user_in_backend(pool_id, username, details=None, raise_if_exists=False):
    # TODO possibly find a better way to store the user info
    region_state = CognitoRegion.get_for_pool(pool_id)
    details = details or region_state.users[pool_id].get(username, {})
    idp_client = connect_for_entity_id('cognito-idp', pool_id)
    user_attrs = details['UserAttributes'] = details.get('UserAttributes', [])

    # add existing sub to attributes
    ensure_sub_in_user(details)

    # determine whether the username is an email/phone alias, then update user attributes
    update_user_attrs_for_aliases(pool_id, username, details)

    existing = get_user_sub_from_username_alias(pool_id, username)
    if raise_if_exists and existing:
        response = error_response('An account with username %s already exists in user pool %s' %
                                  (pool_id, username), error_type='UsernameExistsException')
        raise aws_responses.ErrorResponse(response)

    user_sub = existing or username
    try:
        user_attrs = list(user_attrs)  # create a copy to avoid appending to local attrs
        user_attrs.append({'Name': ATTR_MARKER_INTERNAL_CALL, 'Value': 'test'})
        kwargs = {}
        if details.get('ValidationData', []):
            kwargs['ValidationData'] = details['ValidationData']
        return idp_client.admin_create_user(UserPoolId=pool_id, Username=user_sub,
            UserAttributes=user_attrs, **kwargs)['User']
    except Exception as e:
        regex = r'.*An account with the given [a-zA-Z_\s]+ already exists'
        if 'UsernameExistsException' in str(e) or re.match(regex, str(e)):
            return idp_client.admin_update_user_attributes(
                UserPoolId=pool_id, Username=user_sub, UserAttributes=user_attrs)
        raise


def update_user_attrs_for_aliases(pool_id, username, details):
    """ Update user attributes in case the username is an email/phone alias """
    # See: https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html

    username_orig = username

    user_attrs = details['UserAttributes'] = details.get('UserAttributes', [])
    pool_details = get_user_pool_details(pool_id)
    username_attrs = pool_details.get('UsernameAttributes', [])

    is_email = email_utils.is_email_address(username) and 'email' in username_attrs
    is_phone = is_phone_number(username) and 'phone_number' in username_attrs
    if is_email or is_phone:
        sub = get_sub_from_user_attrs(details)
        if not sub:
            raise Exception('Unable to determine "sub" from user attributes for "%s": %s' % (username, details))

        username = details['Username'] = sub
        attr_key = 'email' if is_email else 'phone_number'
        existing = [a for a in user_attrs if a['Name'] == attr_key]
        user_attrs = details['UserAttributes'] = [a for a in user_attrs if a['Name'] not in ['sub', attr_key]]
        if existing and existing[0]['Value'] != username_orig:
            LOG.info('Overwriting existing "%s" user attribute (value "%s") with new value: %s' %
                     (attr_key, existing[0]['Value'], username_orig))
        user_attrs.append({'Name': attr_key, 'Value': username_orig})
        user_attrs.append({'Name': 'sub', 'Value': sub})


def is_phone_number(value):
    return re.match(r'\+[0-9]{5,50}', (value or '').strip())


def get_user_sub(username, client_id=None, pool_id=None):
    user = find_user(username, client_id=client_id, pool_id=pool_id) or {}
    result = user.get('sub')
    if not result:
        sub_attr = get_sub_from_user_attrs(user)
        if sub_attr:
            result = sub_attr
    if not result:
        LOG.info('Unable to find "sub" attribute for user "%s" in user pool %s: %s' % (username, pool_id, user))
    return result


def get_pool_client(client_id):
    return _get_pool_and_client(client_id)[1]


def get_pool_for_client(client_id):
    return _get_pool_and_client(client_id)[0]


def _get_pool_and_client(client_id):
    # look up from cache
    cached = CLIENT_POOL_CACHE.get(client_id)
    if cached:
        return cached
    idp_client = connect_for_entity_id('cognito-idp', client_id)
    for pool in idp_client.list_user_pools(MaxResults=100)['UserPools']:
        pool_id = pool['Id']
        clients = idp_client.list_user_pool_clients(UserPoolId=pool_id, MaxResults=100)['UserPoolClients']
        client = [c for c in clients if c['ClientId'] == client_id]
        if client:
            CLIENT_POOL_CACHE[client_id] = (pool, client[0])
            return pool, client[0]
    msg = 'Unable to find user pool client with ID %s' % client_id
    LOG.info('%s: %s' % (msg, ''.join(traceback.format_stack())))
    raise Exception(msg)


def get_user_pool_details(pool_id):
    idp_client = connect_for_entity_id('cognito-idp', pool_id)
    return idp_client.describe_user_pool(UserPoolId=pool_id)['UserPool']


def add_custom_claims_from_trigger(pool_id, client_id, result, flow_type=None):
    if not flow_type:
        return
    request_payload = {
        'userAttributes': result,
        'groupConfiguration': {
            'groupsToOverride': [],
            'iamRolesToOverride': [],
            'preferredRole': None
        }
    }
    event = {'request': request_payload}
    flow_type_triggers = {
        'user_auth': cognito_triggers.TRIGGER_TOKEN_AUTH,
        'refresh_token': cognito_triggers.TRIGGER_TOKEN_REFRESH,
        'new_pass': cognito_triggers.TRIGGER_TOKEN_NEW_PASS
    }
    trigger_type = flow_type_triggers[flow_type]
    response = call_cognito_trigger(pool_id, trigger_type, payload=event, client_id=client_id)
    overrides = response.get('response', {}).get('claimsOverrideDetails', {})
    for add_key, add_value in overrides.get('claimsToAddOrOverride', {}).items():
        result[add_key] = add_value
    for to_remove in overrides.get('claimsToSuppress', []):
        result.pop(to_remove, None)


def create_jwt_token(subject, username=None, issuer=None, email=None, iat=None, exp=None, audience=None,
                     attributes=None, client_id=None, token_use=None, pool_id=None, scope=None, flow_type=None):
    iat = int(iat or now_utc())
    exp = exp or (iat + TOKEN_EXPIRY_SECONDS)
    pool_id = get_pool_id(client_id=client_id, pool_id=pool_id)
    issuer = get_issuer_url(client_id=client_id, pool_id=pool_id)
    scope = scope or 'aws.cognito.signin.user.admin'
    token_use = token_use or 'id'
    username = username or subject
    attributes = attributes or {}
    if not subject and username:
        subject = get_user_sub(username, client_id=client_id, pool_id=pool_id)
    payload = {
        'exp': exp,
        'iss': issuer,
        'sub': subject,
        'auth_time': iat,
        'iat': iat,
        'event_id': long_uid(),
        'token_use': token_use
    }
    if token_use == 'id':
        # TODO: add cognito:username also for access tokens?
        if 'cognito:username' not in attributes:
            payload['cognito:username'] = username
    elif token_use == 'access':
        # details for access tokens
        payload['username'] = username
        payload['scope'] = scope
        payload['jti'] = long_uid()
        payload['client_id'] = client_id
    else:
        LOG.warning('Invalid Cognito JWT token_use attribute "%s"' % token_use)

    if email:
        payload['email'] = email
    if audience:
        payload['aud'] = audience
    if 'cognito:groups' not in attributes:
        # list groups for username
        groups = list_groups_for_user(username, pool_id=pool_id, client_id=client_id)
        if groups:
            payload['cognito:groups'] = groups
    for attr, value in attributes.items():
        if attr not in RESERVED_JWT_ATTRIBUTE_NAMES:
            payload[attr] = value

    # call TokenGeneration cognito trigger for identity tokens
    if token_use == 'id':
        add_custom_claims_from_trigger(pool_id, client_id, payload, flow_type=flow_type)

    private_key = to_str(get_test_jwt_keypair()[1].save_pkcs1())
    encoded = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': TEST_JWT_KEY_ID})
    encoded = to_str(encoded)
    return encoded


def get_test_jwt_keypair():
    global TEST_JWT_KEYPAIR
    TEST_JWT_KEYPAIR = TEST_JWT_KEYPAIR or rsa.newkeys(2048)
    return TEST_JWT_KEYPAIR


def get_pool_region(pool_id):
    return pool_id.split('_')[0]


def get_issuer_url(client_id=None, pool_id=None):
    pool_id = get_pool_id(client_id=client_id, pool_id=pool_id)
    issuer = '%s/%s' % (config.TEST_COGNITO_IDP_URL, pool_id)
    return issuer


def is_case_insensitive_pool(pool_id):
    pool_details = get_user_pool_details(pool_id)
    case_sensitive = pool_details.get('UsernameConfiguration', {}).get('CaseSensitive', True)
    return case_sensitive is not True


def lookup_entry_considering_case_insensitivity(pool_id, map, username):
    result = map.get(username)
    if result is not None:
        return result
    case_insensitive = is_case_insensitive_pool(pool_id)
    if not case_insensitive:
        return

    def _matches(key):
        keys = key.values if isinstance(key, MultiKeyDict.MultiKey) else [key]
        for k in keys:
            if str(k).lower() == username_lower:
                return True
    username_lower = str(username).lower()
    result = [k for k in map.keys() if _matches(k)]

    if not result:
        return
    return map.get(result[0])


def get_pool_id(client_id=None, pool_id=None):
    if client_id and not pool_id:
        user_pool = get_pool_client(client_id)
        pool_id = user_pool['UserPoolId']
    return pool_id


def select_valid_pool_client_scopes(scopes, client_id, pool_id=None):
    if not client_id:
        return ''
    pool_id = get_pool_id(client_id=client_id, pool_id=pool_id)
    # TODO: replace by in-memory lookup, once we've moved away from moto backend!
    cognito = aws_stack.connect_to_service('cognito-idp')
    client = cognito.describe_user_pool_client(UserPoolId=pool_id, ClientId=client_id).get('UserPoolClient')
    client_scopes = client.get('AllowedOAuthScopes') or []
    scopes = [s for s in scopes if s in client_scopes]
    scope = ' '.join(scopes)
    return scope


def issue_token(subject=None, username=None, client_id=None, pool_id=None, flow_type=None, scopes=None):
    flow_type = flow_type or 'user_auth'
    scopes = scopes or []
    pool_id = get_pool_id(client_id=client_id, pool_id=pool_id)
    scope = select_valid_pool_client_scopes(scopes, client_id=client_id, pool_id=pool_id)
    access_token = create_jwt_token(
        subject=subject, username=username, client_id=client_id, token_use='access', scope=scope)
    issuer = get_issuer_url(client_id=client_id, pool_id=pool_id)
    try:
        attributes = get_user_attributes(username or subject, pool_id=pool_id)
    except Exception:
        # this can happen, e.g., when creating a token for grant_type=client_credentials OAuth flow
        attributes = {}
    user_email = attributes.get('email')
    id_token = create_jwt_token(
        subject=subject, username=username, audience=client_id, issuer=issuer, email=user_email,
        attributes=attributes, client_id=client_id, token_use='id', pool_id=pool_id, flow_type=flow_type)
    refresh_token = short_uid()
    token = {
        'AccessToken': access_token,
        'ExpiresIn': TOKEN_EXPIRY_SECONDS,
        'TokenType': 'Bearer',
        'RefreshToken': refresh_token,
        'IdToken': id_token
    }
    entry = {
        'subject': subject,
        'username': username,
        'details': token,
        'pool_id': pool_id,
        'client_id': client_id,
        'user_email': user_email,
        'expiry': int(now_utc()) + TOKEN_EXPIRY_SECONDS
    }
    CognitoRegion.REFRESH_TOKENS[refresh_token] = entry
    CognitoRegion.ACCESS_TOKENS[access_token] = entry
    # set access token in cognito backend
    region = get_pool_region(pool_id)
    backend = cognitoidp_models.cognitoidp_backends[region]
    if client_id:
        pool_id = get_pool_for_client(client_id)['Id']
        user_pool = backend.user_pools.get(pool_id)
        if not user_pool:
            raise Exception('Unable to find user pool %s for region %s (existing: %s)' %
                (pool_id, region, list(backend.user_pools.keys())))
        user_pool.access_tokens[access_token] = (client_id, subject)
    token = json_safe(token)
    return token


def is_response_obj(result):
    return isinstance(result, (Response, RequestsResponse))


def get_username_for_hashing(username, client_id=None, pool_id=None):
    # TODO: error handling if pool/client not found
    pool_id = get_pool_id(client_id=client_id, pool_id=pool_id) or ''
    result = '%s%s' % (pool_id.split('_')[-1], username)
    return result


def b64_encode(s):
    return to_str(base64.b64encode(to_bytes(s)))


def base64url_encode(s):
    # see https://tools.ietf.org/html/rfc4648#section-5
    return to_str(base64.urlsafe_b64decode(to_bytes(s))).rstrip('=')


def get_request_from_body_or_query_params(path, data, expected_param=None):
    req_data = parse_query_string(data)
    if not req_data or (expected_param and not req_data.get(expected_param)):
        parsed_path = urlparse.urlparse(path)
        req_data = parse_query_string(parsed_path.query)
    return req_data


def parse_query_string(qs):
    req_data = urlparse.parse_qs(to_str(qs or ''))
    req_data = dict([(k, to_str(v[0])) for k, v in req_data.items()])
    return req_data


def find_user(name, client_id=None, pool_id=None, resolve_alias=True):
    pool_id = get_pool_id(client_id=client_id, pool_id=pool_id)
    region_state = CognitoRegion.get_for_pool(pool_id)

    for _, details in region_state.users.items():
        for uid, user in details.items():
            if name in [user.get('Username'), uid]:
                if user.get('ClientId') == client_id or user.get('UserPoolId') == pool_id:
                    return user
    if not resolve_alias:
        return

    # fall back to finding user by alias
    try:
        canonical_name = get_canonical_username(name, client_id=client_id)
        if name == canonical_name:
            return
        return find_user(canonical_name, client_id, resolve_alias=False)
    except CognitoException as e:
        if 'not exist' not in str(e.message):
            raise


def get_canonical_username(username_or_alias, pool_id=None, client_id=None):
    if not pool_id:
        user_pool = get_pool_client(client_id)
        pool_id = user_pool['UserPoolId']
    user = get_user_for_username_alias(pool_id, username_or_alias)
    return user['Username']


def list_groups_for_user(username, pool_id, client_id):
    try:
        canonical_name = get_canonical_username(username, client_id=client_id)
        cognito = connect_for_entity_id('cognito-idp', pool_id)
        groups = cognito.admin_list_groups_for_user(Username=canonical_name, UserPoolId=pool_id).get('Groups') or []
        groups = [g['GroupName'] for g in groups]
        return groups
    except Exception as e:
        LOG.info('Unable to list Cognito groups for user %s in pool %s: %s' % (username, pool_id, e))
        return []


def error_response(msg, code=400, error_type='Exception'):
    LOG.info(msg)
    result = {'__type': error_type, 'message': msg}
    headers = {
        'x-amzn-errortype': error_type,
        'x-amzn-errormessage': msg,
        'x-amzn-requestid': long_uid()
    }
    return aws_responses.requests_response(result, code, headers=headers)
