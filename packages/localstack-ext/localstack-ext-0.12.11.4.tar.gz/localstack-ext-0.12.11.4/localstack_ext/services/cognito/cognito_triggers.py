import json
from flask import Response
from localstack.utils.aws import aws_stack
from localstack.services.awslambda import lambda_api, lambda_executors

# maps pool IDs to trigger details
COGNITO_TRIGGERS = {}

# Trigger source definitions, see:
# https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
# Sign-up, confirmation, and sign-in (authentication) triggers
TRIGGER_SIGNUP = 'PreSignUp_SignUp'
TRIGGER_ADMIN_CREATE_USER = 'PreSignUp_AdminCreateUser'
TRIGGER_CONFIRM_SIGNUP = 'PostConfirmation_ConfirmSignUp'
TRIGGER_CONFIRM_FORGOT_PW = 'PostConfirmation_ConfirmForgotPassword'
TRIGGER_PRE_AUTH = 'PreAuthentication_Authentication'
TRIGGER_POST_AUTH = 'PostAuthentication_Authentication'
# Custom authentication challenge triggers
TRIGGER_AUTH_DEFINE_CHALL = 'DefineAuthChallenge_Authentication'
TRIGGER_AUTH_CREATE_CHALL = 'CreateAuthChallenge_Authentication'
TRIGGER_AUTH_VERIFY_CHALL = 'VerifyAuthChallengeResponse_Authentication'
# Pre token generation triggers
TRIGGER_TOKEN_HOSTED_AUTH = 'TokenGeneration_HostedAuth'
TRIGGER_TOKEN_AUTH = 'TokenGeneration_Authentication'
TRIGGER_TOKEN_NEW_PASS = 'TokenGeneration_NewPasswordChallenge'
TRIGGER_TOKEN_AUTH_DEVICE = 'TokenGeneration_AuthenticateDevice'
TRIGGER_TOKEN_REFRESH = 'TokenGeneration_RefreshTokens'
# Migrate user triggers
TRIGGER_MIGRATE_AUTH = 'UserMigration_Authentication'
TRIGGER_MIGRATE_FORGOT = 'UserMigration_ForgotPassword'
# Custom message triggers
TRIGGER_CUSTOM_SIGNUP = 'CustomMessage_SignUp'
TRIGGER_CUSTOM_ADMIN_CREATE = 'CustomMessage_AdminCreateUser'
TRIGGER_CUSTOM_RESEND = 'CustomMessage_ResendCode'
TRIGGER_CUSTOM_FORGOT = 'CustomMessage_ForgotPassword'
TRIGGER_CUSTOM_UPDATE_ATTR = 'CustomMessage_UpdateUserAttribute'
TRIGGER_CUSTOM_VERIFY_ATTR = 'CustomMessage_VerifyUserAttribute'
TRIGGER_CUSTOM_AUTH = 'CustomMessage_Authentication'
# Custom message triggers
TRIGGER_CUSTOM_EMAIL_SIGNUP = 'CustomEmailSender_SignUp'
TRIGGER_CUSTOM_EMAIL_ADMIN_CREATE = 'CustomEmailSender_AdminCreateUser'
TRIGGER_CUSTOM_EMAIL_RESEND = 'CustomEmailSender_ResendCode'
TRIGGER_CUSTOM_EMAIL_FORGOT = 'CustomEmailSender_ForgotPassword'
TRIGGER_CUSTOM_EMAIL_UPDATE_ATTR = 'CustomEmailSender_UpdateUserAttribute'
TRIGGER_CUSTOM_EMAIL_VERIFY_ATTR = 'CustomEmailSender_VerifyUserAttribute'
TRIGGER_CUSTOM_EMAIL_TAKE_OVER = 'CustomEmailSender_AccountTakeOverNotification'


def call_cognito_trigger(pool_id, trigger, client_id=None, payload={}):
    cognito = aws_stack.connect_to_service('cognito-idp', region_name=get_pool_region(pool_id))
    pool_details = cognito.describe_user_pool(UserPoolId=pool_id)['UserPool']
    lambda_config = pool_details.get('LambdaConfig', {})
    trigger_orig = trigger

    for search, replace in (('', ''), ('CustomMessage_', 'CustomEmailSender_')):
        trigger = trigger_orig.replace(search, replace)
        trigger_type = trigger.split('_')[0]
        # lambda config is PreTokenGeneration, but trigger names are named TokenGeneration_*
        trigger_type = trigger_type.replace('Token', 'PreToken')
        trigger_lambda = lambda_config.get(trigger_type)
        if trigger_lambda:
            break

    if not trigger_lambda:
        return {}
    client_id = client_id or 'CLIENT_ID_NOT_APPLICABLE'
    event = {
        'version': '$LATEST',
        'triggerSource': trigger,
        'region': aws_stack.get_region(),
        'userPoolId': pool_id,
        'callerContext': {
            'awsSdkVersion': 'TODO',
            'clientId': client_id
        },
        'request': {
            'userAttributes': {},
            'validationData': {},
            'clientMetadata': {}
        },
        'response': {}
    }
    request_payload = payload.pop('request', None) or {}
    event['request'].update(request_payload)
    event.update(payload)
    result = lambda_api.run_lambda(event=event, context={}, func_arn=trigger_lambda)
    result = result.result if isinstance(result, lambda_executors.InvocationResult) else result
    if isinstance(result, Response) and result.status_code >= 400:
        raise Exception('Error running Cognito trigger Lambda "%s": %s' % (trigger_lambda, result.data))
    result = result if isinstance(result, (dict, Response)) else json.loads(result)
    return result


def get_pool_region(pool_id):
    return pool_id.split('_')[0]
