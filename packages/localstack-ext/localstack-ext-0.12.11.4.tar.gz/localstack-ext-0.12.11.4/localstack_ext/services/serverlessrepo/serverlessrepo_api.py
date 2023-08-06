import io
import os
import re
import json
import yaml
import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from localstack import config
from localstack.utils.aws import aws_stack
from localstack.utils.common import (
    short_uid, first_char_to_lower, clone, timestamp_millis, load_file, keys_to_lower, to_bytes)
from localstack.services.generic_proxy import serve_flask_app
from localstack.utils.aws.aws_responses import flask_error_response_json
from localstack_ext.utils.aws import aws_utils
from localstack_ext.services.base import RegionBackend

APP_NAME = 'servicediscovery_api'
app = Flask(APP_NAME)
CORS(app)

LOG = logging.getLogger(__name__)

S3_BUCKET_ARTIFACTS = 'ls--serverlessrepo--artifacts'

PATH_REGEX_PREFIX = '^/?applications(/[^/:]+|(/[^/]+applications/[^/]+))?'
PATH_REGEX_APPS = '%s$' % PATH_REGEX_PREFIX
PATH_REGEX_APP_VERSIONS = '%s/versions(/[^/]+)?$' % PATH_REGEX_PREFIX
PATH_REGEX_CHANGESETS = '%s/changesets$' % PATH_REGEX_PREFIX
PATH_REGEX_TEMPLATES = '%s/templates(/[^/]+)?$' % PATH_REGEX_PREFIX

THIS_FOLDER = os.path.dirname(__file__)
EXISTING_REPOS_FILE = os.path.join(THIS_FOLDER, 'existing.repos.yml')

# List of predefined apps from here: https://serverlessrepo.aws.amazon.com/
PREDEFINED_APPS = [
    'arn:aws:serverlessrepo:us-east-1:297356227824:applications/SecretsManagerRDSPostgreSQLRotationMultiUser'
]


class ServerlessRepoRegion(RegionBackend):
    def __init__(self):
        # maps application ID to application details
        self.applications = {}


class ServerlessApplication(object):
    def __init__(self, metadata={}):
        self.metadata = metadata
        # list of application version details
        self.versions = []
        # maps template ID to template details
        self.templates = {}
        # maps stack names to list of change sets
        self.change_sets = {}


# --------------
# API ENDPOINTS
# --------------

def create_application(data):
    region = ServerlessRepoRegion.get()
    app_id = data['applicationId'] = aws_utils.serverlessrepo_app_arn(short_uid())
    app = ServerlessApplication(data)
    region.applications[app_id] = app
    return data


def list_applications():
    region = ServerlessRepoRegion.get()
    result = [a.metadata for a in region.applications.values()]
    result = {'applications': result}
    return result


def list_application_versions(path):
    app = lookup_application(path)
    if isinstance(app, Response):
        return app
    result = {'versions': list(app.versions)}
    return result


def create_application_version(path, data):
    app = lookup_application(path)
    if isinstance(app, Response):
        return app
    data['applicationId'] = app.metadata['applicationId']
    app.versions.append(data)
    return data


def create_cloud_formation_template(path, data):
    app = lookup_application(path)
    if isinstance(app, Response):
        return app
    app_id = app.metadata['applicationId']
    sem_ver = data.get('semanticVersion')
    data['applicationId'] = app_id
    version_obj = ([v for v in app.versions if v.get('semanticVersion') == sem_ver] or [{}])[0]
    if not version_obj:
        version_obj = app.versions[-1]
        if sem_ver:
            LOG.info('Unable to find Serverless app "%s" version "%s" - defaulting to %s' % (
                app_id, sem_ver, version_obj['semanticVersion']))
    result = clone(data)
    result['templateUrl'] = version_obj.get('templateUrl') or app.metadata.get('templateUrl')
    result['templateId'] = tmpl_id = short_uid()
    result['status'] = 'ACTIVE'
    result['creationTime'] = timestamp_millis()
    app.templates[tmpl_id] = result
    return result


def get_cloud_formation_template(path):
    app = lookup_application(path)
    if isinstance(app, Response):
        return app
    tmpl_id = re.match(PATH_REGEX_TEMPLATES, path).group(3).strip('/')
    result = app.templates.get(tmpl_id)
    if not result:
        return not_found_error('Unable to find CloudFormation template "%s" for Serverless app "%s"' % (
            tmpl_id, app.metadata['applicationId']))
    return result


def create_cloud_formation_change_set(path, data):
    stack_name = data.get('stackName')
    app = lookup_application(path)
    if isinstance(app, Response):
        return app
    app.change_sets[stack_name] = change_sets = app.change_sets.get(stack_name) or []
    change_sets.append(data)

    # deploy stack via CloudFormation
    client = aws_stack.connect_to_service('cloudformation')
    kwargs = {}
    params = ['ChangeSetName', 'ClientToken', 'Description', 'NotificationArns',
        'ResourceTypes', 'RollbackConfiguration', 'StackName', 'Tags']
    for param in params:
        param_lower = first_char_to_lower(param)
        value = data.get(param_lower)
        if value is not None:
            kwargs[param_lower] = value
    result = client.create_change_set(**kwargs)

    result = {
        'applicationId': app.metadata['applicationId'],
        'changeSetId': result['Id'],
        'semanticVersion': data.get('semanticVersion'),
        'stackId': result['StackId']
    }
    return result


def lookup_application(path):
    region = ServerlessRepoRegion.get()
    regex = '%s($|/)' % PATH_REGEX_PREFIX
    app_id = re.match(regex, path).group(1).strip('/')
    app = region.applications.get(app_id)

    def get_predefined_app():
        if app_id not in PREDEFINED_APPS:
            return
        existing_repos = load_existing_repos()
        existing = existing_repos.get(app_id)
        if not existing:
            return
        LOG.info('Found reference to predefined repo "%s"' % app_id)
        existing = keys_to_lower(existing)
        version = existing.pop('version', None)
        app = ServerlessApplication(existing)
        region.applications[app_id] = app
        if version:
            app.versions.append(version)
            # upload template body to S3
            tmpl_body = version.pop('templateBody', None)
            if tmpl_body:
                aws_stack.get_or_create_bucket(S3_BUCKET_ARTIFACTS)
                s3_client = aws_stack.connect_to_service('s3')
                s3_client.upload_fileobj(io.BytesIO(to_bytes(tmpl_body)), S3_BUCKET_ARTIFACTS, app_id)
                existing['templateUrl'] = get_s3_download_url(S3_BUCKET_ARTIFACTS, app_id)
        return app

    app = app or get_predefined_app()
    return app or not_found_error('Unable to find Serverless app with ID "%s"' % app_id)


def get_s3_download_url(bucket, key):
    return '%s/%s/%s' % (config.get_edge_url(), bucket, key)


def load_existing_repos():
    result = yaml.load(load_file(EXISTING_REPOS_FILE))
    result = {r['ApplicationId']: r for r in result}
    return result


# --------------
# MAIN ENDPOINT
# --------------

@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def main_entrypoint(path):
    action = request.headers.get('x-amz-target', '')
    action = action.split('.')[-1]
    method = request.method
    data = json.loads(request.get_data() or '{}')

    result = None
    if re.match(PATH_REGEX_CHANGESETS, path):
        if method == 'POST':
            result = create_cloud_formation_change_set(path, data)
    elif re.match(PATH_REGEX_TEMPLATES, path):
        if method == 'POST':
            result = create_cloud_formation_template(path, data)
        if method == 'GET':
            result = get_cloud_formation_template(path)
    elif re.match(PATH_REGEX_APP_VERSIONS, path):
        if method == 'GET':
            result = list_application_versions(path)
        if method == 'PUT':
            result = create_application_version(path, data)
    elif re.match(PATH_REGEX_APPS, path):
        if method == 'GET':
            result = list_applications()
        if method == 'POST':
            result = create_application(data)
    if result is None:
        LOG.debug('Unsupported Serverless Application Repository action "%s %s"' % (method, path))
        return not_found_error()

    result = jsonify(result) if isinstance(result, dict) else result
    return result


def not_found_error(msg=None):
    msg = msg or 'The specified resource doesnt exist.'
    return flask_error_response_json(msg, code=404, error_type='ResourceNotFoundException')


def serve(port, quiet=True):
    return serve_flask_app(app=app, port=port, quiet=quiet)
