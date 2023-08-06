import json
import logging
from localstack.constants import TEST_AWS_ACCOUNT_ID
from localstack.utils.aws import aws_stack
from localstack.utils.common import to_str
from localstack.utils.analytics import event_publisher
from localstack.services.generic_proxy import ProxyListener
from localstack.utils.aws.aws_responses import requests_error_response_json
from localstack_ext.services.glue import job_executor

LOG = logging.getLogger(__name__)

EVENT_TYPE_CREATE_JOB = 'glu.cj'
EVENT_TYPE_CREATE_CRAWLER = 'glu.cc'

CLASSIFIER_TYPES = ['GrokClassifier', 'XMLClassifier', 'JsonClassifier', 'CsvClassifier']

# maps region names to details
REGIONS = {}


class GlueRegion(object):
    def __init__(self):
        # maps names to job details
        self.jobs = {}
        # maps run IDs to job run details
        self.job_runs = {}
        # maps names to crawler details
        self.crawlers = {}
        # maps names to classifier details
        self.classifiers = {}
        # maps names to trigger details
        self.triggers = {}
        # maps names to workflow details
        self.workflows = {}
        # maps names to database details
        self.databases = {}
        # maps db_name -> table_name -> table_details
        self.db_tables = {}

    @staticmethod
    def get():
        region = aws_stack.get_region()
        instance = REGIONS[region] = REGIONS.get(region) or GlueRegion()
        return instance


def get_job(data):
    region = GlueRegion.get()
    result = region.jobs.get(data['JobName'])
    if not result:
        return error_response('Unable to find Glue job named "%s"' % data['JobName'], code=404)
    return {'Job': result}


def create_job(data):
    region = GlueRegion.get()
    job_name = data['Name']
    event_publisher.fire_event(EVENT_TYPE_CREATE_JOB,
        payload={'n': event_publisher.get_hash(job_name)})
    region.jobs[job_name] = data
    return {'Name': job_name}


def list_jobs():
    region = GlueRegion.get()
    result = {'JobNames': [j['Name'] for j in region.jobs.values()]}
    return result


def get_crawler(data):
    region = GlueRegion.get()
    result = region.crawlers.get(data['Name'])
    if not result:
        return error_response('Unable to find Glue crawler named "%s"' % data['Name'], code=404)
    return {'Crawler': result}


def create_crawler(data):
    region = GlueRegion.get()
    crawler_name = data['Name']
    event_publisher.fire_event(EVENT_TYPE_CREATE_CRAWLER,
        payload={'n': event_publisher.get_hash(crawler_name)})
    region.crawlers[crawler_name] = data
    return {}


def get_database(data):
    region = GlueRegion.get()
    result = region.databases.get(data['Name'])
    catalog_id = data.get('CatalogId')
    if not result or (catalog_id and catalog_id != result.get('CatalogId')):
        return 404
    return {'Database': result}


def get_databases(data):
    region = GlueRegion.get()
    result = list(region.databases.value())
    return {'DatabaseList': result}


def create_database(data):
    region = GlueRegion.get()
    database = data.get('DatabaseInput', {})
    database['catalog_id'] = data.get('CatalogId') or TEST_AWS_ACCOUNT_ID
    db_name = database.get('Name')
    region.databases[db_name] = data
    return {}


def get_classifier(data):
    region = GlueRegion.get()
    result = region.classifiers.get(data['Name'])
    if not result:
        return error_response('Unable to find Glue classifier named "%s"' % data['Name'], code=404)
    return {'Classifier': result}


def create_classifier(data):
    region = GlueRegion.get()
    for clf in CLASSIFIER_TYPES:
        if clf in data:
            clf_name = data[clf]['Name']
            region.classifiers[clf_name] = {clf: data[clf]}
    return {}


def get_trigger(data):
    region = GlueRegion.get()
    result = region.triggers.get(data['Name'])
    if not result:
        return error_response('Unable to find Glue trigger named "%s"' % data['Name'], code=404)
    return {'Trigger': result}


def create_trigger(data):
    region = GlueRegion.get()
    tr_name = data['Name']
    region.triggers[tr_name] = data
    return {}


def get_table(data):
    region = GlueRegion.get()
    db_name = data['DatabaseName']
    result = region.db_tables.get(db_name, {}).get(data['Name'])
    catalog_id = data.get('CatalogId')
    if not result or (catalog_id and catalog_id != result.get('CatalogId')):
        return error_response('Unable to find Glue table "%s" in DB "%s", catalog "%s"' %
            (data['Name'], db_name, catalog_id), code=404)
    return {'Table': result}


def get_tables(data):
    region = GlueRegion.get()
    db_name = data['DatabaseName']
    result = region.db_tables.get(db_name, {}).values()
    catalog_id = data.get('CatalogId')
    result = [t for t in result if catalog_id in [t.get('CatalogId'), None]]
    return {'TableList': result}


def create_table(data):
    region = GlueRegion.get()
    tab_name = data['TableInput'].get('Name')
    db_name = data['DatabaseName']
    region.db_tables[db_name] = region.db_tables.get(db_name) or {}
    if tab_name in region.db_tables[db_name]:
        return error_response('Glue table named "%s" already exists in DB "%s"' % (tab_name, db_name), code=400)
    region.db_tables[db_name][tab_name] = data
    return {}


def get_workflow(data):
    region = GlueRegion.get()
    result = region.workflows.get(data['Name'])
    if not result:
        return error_response('Unable to find Glue workflow named "%s"' % data['Name'], code=404)
    return {'Workflow': result}


def create_workflow(data):
    region = GlueRegion.get()
    wf_name = data['Name']
    region.workflows[wf_name] = data
    return {}


def start_job_run(data):
    job_name = data['JobName']
    region = GlueRegion.get()
    job_details = region.jobs.get(job_name)
    if not job_details:
        return error_response('Unable to find Glue job named "%s"' % job_name, code=404)
    run_id = job_executor.start_job_run(job_details)
    result = {'JobRunId': run_id}
    return result


class ProxyListenerGlue(ProxyListener):

    def forward_request(self, method, path, data, headers):
        if method == 'OPTIONS':
            return 200

        action = headers.get('X-Amz-Target', '').split('.')[-1]
        data = json.loads(to_str(data or '{}'))

        # print('glue', method, path, action, data, headers)

        if action == 'ListJobs':
            return list_jobs()
        elif action == 'CreateJob':
            return create_job(data)
        elif action == 'GetJob':
            return get_job(data)
        elif action == 'GetCrawler':
            return get_crawler(data)
        elif action == 'CreateCrawler':
            return create_crawler(data)
        elif action == 'GetDatabase':
            return get_database(data)
        elif action == 'GetDatabases':
            return get_databases(data)
        elif action == 'CreateDatabase':
            return create_database(data)
        elif action == 'GetTable':
            return get_table(data)
        elif action == 'GetTables':
            return get_tables(data)
        elif action == 'CreateTable':
            return create_table(data)
        elif action == 'GetClassifier':
            return get_classifier(data)
        elif action == 'CreateClassifier':
            return create_classifier(data)
        elif action == 'GetTrigger':
            return get_trigger(data)
        elif action == 'CreateTrigger':
            return create_trigger(data)
        elif action == 'GetWorkflow':
            return get_workflow(data)
        elif action == 'CreateWorkflow':
            return create_workflow(data)
        elif action == 'StartJobRun':
            return start_job_run(data)

        return True


# -----------------
# HELPER FUNCTIONS
# -----------------

def error_response(msg, code=400, error_type='Exception'):
    if code != 404:
        LOG.warning(msg)
    error_type = 'ResourceNotFound' if code == 404 else error_type
    return requests_error_response_json(msg, code=code, error_type=error_type)


# instantiate listener
UPDATE_GLUE = ProxyListenerGlue()
