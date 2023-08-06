import logging
import traceback
import xmltodict
from flask import Flask, request, make_response
from flask_cors import CORS
from localstack.utils.common import short_uid, clone
from localstack.services.generic_proxy import serve_flask_app
from localstack_ext.utils.aws import aws_utils
from localstack_ext.services.base import RegionBackend

APP_NAME = 'elasticbeanstalk_api'
app = Flask(APP_NAME)
CORS(app)

XMLNS = 'https://elasticbeanstalk.amazonaws.com/docs/2010-12-01/'

LOG = logging.getLogger(__name__)


class ElasticBeanstalkRegion(RegionBackend):
    def __init__(self):
        # maps application name to application details
        self.applications = {}
        # maps (platform_name, platform_version) -> platform details
        self.platforms = {}


class Application(object):
    def __init__(self, metadata=None):
        self.metadata = metadata or {}
        # maps version label to version details
        self.versions = {}
        # maps version label to version details
        self.environments = {}


# -----
# UTIL
# -----

def make_api_response(result, operation, status_code=200):
    body = """
        <{op}Response xmlns="{ns}">
            <{op}Result>
                %s
            </{op}Result>
        </{op}Response>
    """.format(ns=XMLNS, op=operation)
    result = result or {}
    body = body % xmltodict.unparse(result, full_document=False)
    body = body.strip()
    return make_response(body), status_code


def make_api_error(message=None, status_code=400, code_string='InvalidParameter'):
    message = message or code_string
    content = """<ErrorResponse xmlns="{xmlns}"><Error>
        <Type>Sender</Type>
        <Code>{code_string}</Code>
        <Message>{message}</Message>
        </Error><RequestId>{req_id}</RequestId>
        </ErrorResponse>""".format(xmlns=XMLNS, message=message, code_string=code_string, req_id=short_uid())
    return make_response(content), status_code


def not_found_error(message, code_string=None):
    return make_api_error(message, code_string=code_string or 'ResourceNotFoundError', status_code=404)


# ------------
# API METHODS
# ------------

# applications

def create_application():
    return create_entity('Application', 'applications')


def describe_applications():
    result = describe_entities('Application', 'applications')
    # TODO: filter by ApplicationName parameter!
    return result


def update_application():
    return modify_entity('Application', 'applications')


def delete_application():
    return delete_entity('Application', 'applications')


# application versions

def create_app_version():
    return create_entity('ApplicationVersion', 'versions',
        id_attr='VersionLabel', parent_id_attr='ApplicationName')


def describe_app_versions():
    result = describe_entities('ApplicationVersion', 'versions',
        id_attr='VersionLabel', parent_id_attr='ApplicationName')
    region_state = ElasticBeanstalkRegion.get()
    data = clone(request.form)
    result = []
    app_name = data.get('ApplicationName')
    labels = data.get('VersionLabels', [])
    for key, application in region_state.applications.items():
        if app_name and key != app_name:
            continue
        for label, version in application.versions.items():
            if labels and label not in labels:
                continue
            result.append(version)
    result = {'member': result}
    return {'ApplicationVersions': result}


def update_app_version():
    return modify_entity('ApplicationVersion', 'versions',
        id_attr='VersionLabel', parent_id_attr='ApplicationName')


def delete_app_version():
    return delete_entity('ApplicationVersion', 'versions',
        id_attr='VersionLabel', parent_id_attr='ApplicationName')


# environments

def create_environment():
    result = create_entity('Environment', 'environments',
        id_attr='EnvironmentId', parent_id_attr='ApplicationName')
    return result['Environment']


def describe_environments():
    result = describe_entities('Environment', 'environments',
        id_attr='EnvironmentId', parent_id_attr='ApplicationName')
    region_state = ElasticBeanstalkRegion.get()
    data = clone(request.form)
    result = []
    app_name = data.get('ApplicationName')
    env_names = data.get('EnvironmentNames', [])
    env_ids = data.get('EnvironmentIds', [])
    for key, application in region_state.applications.items():
        if app_name and key != app_name:
            continue
        for env_id, env_details in application.environments.items():
            if env_names and env_details['EnvironmentName'] not in env_names:
                continue
            if env_ids and env_details['EnvironmentId'] not in env_ids:
                continue
            result.append(env_details)
    result = {'member': result}
    return {'Environments': result}


def update_environment():
    data = clone(request.form)
    error = _assign_environment_id_for_name(data)
    if error is not None:
        return error
    return modify_entity('Environment', 'environments',
        id_attr='EnvironmentId', parent_id_attr='ApplicationName', data=data)


def delete_environment_configuration():
    data = clone(request.form)
    error = _assign_environment_id_for_name(data)
    if error is not None:
        return error
    return delete_entity('Environment', 'environments',
        id_attr='EnvironmentId', parent_id_attr='ApplicationName', data=data)


def _assign_environment_id_for_name(data):
    if data.get('EnvironmentId'):
        return
    region_state = ElasticBeanstalkRegion.get()
    app_name = data.get('ApplicationName', '')
    app = region_state.applications.get(app_name)
    if not app:
        return not_found_error('Unable to find ElasticBeanstalk app named "%s"' % app_name)
    environ = [env for env in app.environments.values() if env['EnvironmentName'] == data.get('EnvironmentName')]
    if not environ:
        return not_found_error('Unable to find ElasticBeanstalk environment "%s" for app "%s"' %
                (data.get('EnvironmentName'), app_name))
    data['EnvironmentId'] = environ[0]['EnvironmentId']


# ----------------------------
# GENERIC API IMPLEMENTATIONS
# ----------------------------

def create_entity(entity_type, entity_map_name, id_attr=None, data=None, parent_id_attr=None):
    data = data or clone(request.form)
    id_attr = id_attr or '%sName' % entity_type
    entity_id = data[id_attr] = data.get(id_attr) or short_uid()
    entity_map = lookup_entity_map(parent_id_attr, entity_map_name, data)
    entity = Application(data) if entity_type == 'Application' else data
    entity_map[entity_id] = entity
    arn_func = getattr(aws_utils, 'elasticbeanstalk_%s_arn' % entity_map_name.replace('_', '').rstrip('s'), None)
    if arn_func:
        parent_entity_id = data.get(parent_id_attr or '')
        args = ([parent_entity_id] if parent_entity_id else []) + [entity_id]
        data['ARN'] = arn_func(*args)
    result = {entity_type: data}
    return result


def delete_entity(entity_type, entity_map_name, id_attr=None, parent_id_attr=None, data=None):
    data = data or clone(request.form)
    id_attr = id_attr or '%sName' % entity_type
    entity_id = data.get(id_attr)
    entity_map = lookup_entity_map(parent_id_attr, entity_map_name, data)
    deleted = entity_map.pop(entity_id, None)
    if not deleted:
        return not_found_error('Unable to find "%s" entity named "%s"' % (entity_type, entity_id))
    return {}


def modify_entity(entity_type, entity_map_name, id_attr=None, data=None, parent_id_attr=None):
    data = data or clone(request.form)
    id_attr = id_attr or '%sName' % entity_type
    entity_id = data.get(id_attr)
    entity_map = lookup_entity_map(parent_id_attr, entity_map_name, data)
    existing = entity_map.get(entity_id)
    if not existing:
        return not_found_error('Unable to find "%s" entity named "%s"' % (entity_type, entity_id))
    existing = getattr(existing, 'metadata', existing)
    existing.update(data)
    result = {entity_type: existing}
    return result


def describe_entities(entity_type, entity_map_name, id_attr=None, parent_id_attr=None):
    data = clone(request.form)
    id_attr = id_attr or '%sName' % entity_type
    entity_id = data.get(id_attr)
    entity_map = lookup_entity_map(parent_id_attr, entity_map_name, data)
    result = [entity for entity in entity_map.values()]
    if entity_id:
        result = [entity for entity in result if entity[id_attr] == entity_id]
    result = [getattr(entity, 'metadata', entity) for entity in result]
    result = {'member': result}
    result = {'%ss' % entity_type: result}
    return result


def lookup_entity_map(parent_id_attr, entity_map_name, data):
    region_state = ElasticBeanstalkRegion.get()
    entity_map_holder = region_state
    parent_entity_id = data.get(parent_id_attr or '')
    if parent_entity_id:
        entity_map_holder = region_state.applications.get(parent_entity_id)
    return getattr(entity_map_holder, entity_map_name)


# -----
# MAIN
# -----

ACTIONS_MAP = {
    'CreateApplication': create_application,
    'CreateApplicationVersion': create_app_version,
    'CreateEnvironment': create_environment,
    'DescribeApplications': describe_applications,
    'DescribeApplicationVersions': describe_app_versions,
    'DescribeEnvironments': describe_environments,
    'DeleteApplication': delete_application,
    'DeleteApplicationVersion': delete_app_version,
    'DeleteEnvironmentConfiguration': delete_environment_configuration,
    'UpdateApplication': update_application,
    'UpdateApplicationVersion': update_app_version,
    'UpdateEnvironment': update_environment
}


@app.route('/', methods=['POST'])
def handle_request():
    try:
        action = request.form.get('Action')
        result = {}

        action_func = ACTIONS_MAP.get(action)
        if action_func:
            result = action_func()
        else:
            msg = 'Unsupported ElasticBeanstalk API action: %s' % action
            LOG.warning(msg)
            return not_found_error(msg)

        if result and not isinstance(result, dict):
            return result
        return make_api_response(result, action)
    except Exception as e:
        LOG.warning('Error handling request: %s %s' % (e, traceback.format_exc()))
        return make_api_error(code_string='Unknown error: %s' % e, status_code=500)


def serve(port, quiet=True):
    return serve_flask_app(app=app, port=port, quiet=quiet)
