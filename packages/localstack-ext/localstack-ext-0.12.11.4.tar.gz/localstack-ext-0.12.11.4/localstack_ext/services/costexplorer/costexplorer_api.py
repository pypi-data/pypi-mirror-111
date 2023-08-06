import json
import logging
from requests.models import Response as RequestsResponse
from flask import Flask, request, make_response, jsonify, Response as FlaskResponse
from localstack.utils.common import to_str, short_uid
from localstack.services.generic_proxy import serve_flask_app
from localstack.utils.aws.aws_responses import requests_to_flask_response
from localstack_ext.utils.aws import aws_utils
from localstack_ext.services.base import RegionBackend, GenericEntityManager

LOG = logging.getLogger(__name__)

APP_NAME = 'costexplorer_api'
app = Flask(APP_NAME)

# string constants
ACTION_PREFIX = 'AWSInsightsIndexService.'


class CostExplorerRegion(RegionBackend):

    def __init__(self):
        # maps category ARN to cost category details
        self.cost_categories = {}
        # maps subscription ARN to anomaly subscription details
        self.anomaly_subscriptions = {}
        # maps monitor ARN to anomaly monitor details
        self.anomaly_monitors = {}


# generic entity manager instance
ENTITY_MANAGER = GenericEntityManager(CostExplorerRegion)


# ------------
# API METHODS
# ------------

def create_cost_category_definition(data):
    data['CostCategoryArn'] = cat_arn = aws_utils.costexplorer_category_arn(data['Name'])
    ENTITY_MANAGER.create_entity('cost_categories', data, id_attr='CostCategoryArn')
    return {'CostCategoryArn': cat_arn}


def describe_cost_category_definition(data):
    return ENTITY_MANAGER.get_entity('cost_categories', data, id_attr='CostCategoryArn')


def update_cost_category_definition(data):
    ENTITY_MANAGER.update_entity('cost_categories', data, id_attr='CostCategoryArn')
    return {'CostCategoryArn': data['CostCategoryArn']}


def delete_cost_category_definition(data):
    ENTITY_MANAGER.delete_entity('cost_categories', data, id_attr='CostCategoryArn')
    return {'CostCategoryArn': data['CostCategoryArn']}


def create_anomaly_subscription(data):
    data = data.get('AnomalySubscription', {})
    if not data.get('SubscriptionArn'):
        data['SubscriptionArn'] = aws_utils.costexplorer_anomaly_subscription_arn(short_uid())
    ENTITY_MANAGER.create_entity('anomaly_subscriptions', data, id_attr='SubscriptionArn')
    return {'SubscriptionArn': data['SubscriptionArn']}


def get_anomaly_subscriptions(data):
    # TODO add filtering!
    return ENTITY_MANAGER.list_entities('anomaly_subscriptions', data)


def update_anomaly_subscription(data):
    ENTITY_MANAGER.update_entity('anomaly_subscriptions', data, id_attr='SubscriptionArn')
    return {'SubscriptionArn': data['SubscriptionArn']}


def describe_anomaly_subscription(data):
    return ENTITY_MANAGER.get_entity('anomaly_subscriptions', data, id_attr='SubscriptionArn')


def delete_anomaly_subscription(data):
    result = ENTITY_MANAGER.delete_entity('anomaly_subscriptions', data, id_attr='SubscriptionArn')
    if isinstance(result, dict):
        return {}
    return result


def create_anomaly_monitor(data):
    data = data.get('AnomalyMonitor')
    if not data.get('MonitorArn'):
        data['MonitorArn'] = aws_utils.costexplorer_anomaly_monitor(short_uid())
    ENTITY_MANAGER.create_entity('anomaly_monitors', data, id_attr='MonitorArn')
    return {'MonitorArn': data['MonitorArn']}


def get_anomaly_monitors(data):
    # TODO add filtering by MonitorArnList!
    return ENTITY_MANAGER.list_entities('anomaly_monitors', data)


def update_anomaly_monitor(data):
    ENTITY_MANAGER.update_entity('anomaly_monitors', data, id_attr='MonitorArn')
    return {'MonitorArn': data['MonitorArn']}


def delete_anomaly_monitor(data):
    result = ENTITY_MANAGER.delete_entity('anomaly_monitors', data, id_attr='MonitorArn')
    if isinstance(result, dict):
        return {}
    return result


# ----------------
# API ENTRY POINT
# ----------------

ACTIONS_MAP = {
    'CreateAnomalyMonitor': create_anomaly_monitor,
    'CreateAnomalySubscription': create_anomaly_subscription,
    'CreateCostCategoryDefinition': create_cost_category_definition,
    'DeleteAnomalyMonitor': delete_anomaly_monitor,
    'DeleteAnomalySubscription': delete_anomaly_subscription,
    'DeleteCostCategoryDefinition': delete_cost_category_definition,
    'DescribeAnomalySubscription': describe_anomaly_subscription,
    'DescribeCostCategoryDefinition': describe_cost_category_definition,
    'GetAnomalySubscriptions': get_anomaly_subscriptions,
    'GetAnomalyMonitors': get_anomaly_monitors,
    'UpdateAnomalySubscription': update_anomaly_subscription,
    'UpdateAnomalyMonitor': update_anomaly_monitor,
    'UpdateCostCategoryDefinition': update_cost_category_definition
}


@app.route('/', methods=['POST'])
def api_entrypoint():
    action = request.headers.get('x-amz-target')
    result = {}
    data = to_str(request.data or '')
    data = json.loads(data)

    # get function from stripped action/target name
    action = action.replace(ACTION_PREFIX, '')
    action_func = ACTIONS_MAP.get(action)

    if not action_func:
        LOG.warning('API method %s currently not implemented' % action)
        return jsonify(result), 404

    # invoke function to get final result
    result = action_func(data)

    if isinstance(result, RequestsResponse):
        return requests_to_flask_response(result)
    if isinstance(result, FlaskResponse):
        return result

    return jsonify(result)


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def fallback(path):
    msg = 'Not yet implemented: Unable to find path mapping for %s /%s' % (request.method, path)
    LOG.warning(msg)
    return make_response(msg), 404


# ---------------
# HELPER METHODS
# ---------------

# TODO: move into utils!
def error_response(msg, code=400, error_type='Exception'):
    LOG.warning(msg)
    result = {'Type': 'User', 'message': msg}
    headers = {'x-amzn-errortype': error_type}
    return make_response((jsonify(result), code, headers))


def not_found_error(msg):
    return error_response(msg, code=404, error_type='ResourceNotFoundException')


def serve(port, quiet=True):
    return serve_flask_app(app=app, port=port, quiet=quiet)
