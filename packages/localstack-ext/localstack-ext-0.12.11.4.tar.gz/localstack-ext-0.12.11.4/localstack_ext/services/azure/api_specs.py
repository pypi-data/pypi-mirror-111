import os
import glob
import json
from localstack import config
from localstack.utils.common import rm_rf, download, load_file, mkdir
from localstack.services.install import download_and_extract_with_retry
from localstack_ext.services.azure.azure_utils import get_matching_paths, log

SPECS = {
    'eventhub-hubs': 'eventhub/resource-manager/Microsoft.EventHub/stable/2017-04-01/eventhubs.json',
    'eventhub-namespaces': 'eventhub/resource-manager/Microsoft.EventHub/stable/2017-04-01/namespaces.json',
    'eventhub-authrules': 'eventhub/resource-manager/Microsoft.EventHub/stable/2017-04-01/AuthorizationRules.json',
    'eventhub-consumergroups': 'eventhub/resource-manager/Microsoft.EventHub/stable/2017-04-01/consumergroups.json',
    'storage-accounts': 'storage/resource-manager/Microsoft.Storage/stable/2019-06-01/storage.json',
    'storage-blob': {
        'storage-dataplane-preview': 'storage/data-plane/Microsoft.BlobStorage/preview/2019-12-12/blob.json'
    },
    'storage-queue': {
        'storage-dataplane-preview': 'storage/data-plane/Microsoft.QueueStorage/preview/2018-03-28/queue.json'
    },
    'subscriptions': 'subscription/resource-manager/Microsoft.Subscription/stable/2020-09-01/subscriptions.json',
    'web-apps': 'web/resource-manager/Microsoft.Web/stable/2020-06-01/WebApps.json',
    'web-resources': 'web/resource-manager/Microsoft.Web/stable/2020-06-01/ResourceProvider.json',
    'service-plans': 'web/resource-manager/Microsoft.Web/stable/2020-06-01/AppServicePlans.json',
    'resource-groups': 'resources/resource-manager/Microsoft.Resources/stable/2020-10-01/resources.json',
    'resource-graph': 'resourcegraph/resource-manager/Microsoft.ResourceGraph/stable/2019-04-01/resourcegraph.json',
    'appinsights-components':
        'applicationinsights/resource-manager/Microsoft.Insights/stable/2015-05-01/components_API.json',
    'devops': 'devops/resource-manager/Microsoft.DevOps/preview/2020-07-13-preview/devops.json',
    'servicebus': 'servicebus/resource-manager/Microsoft.ServiceBus/stable/2017-04-01/eventhubs.json'
}

# spec ZIP URL
DOWNLOAD_FULL_SPECS = False
SPEC_ZIP_URL = 'https://github.com/Azure/azure-rest-api-specs/archive/master.zip'
GITHUB_AZURE_SPECS_URL = 'https://raw.githubusercontent.com/Azure/azure-rest-api-specs/<branch>/'

# additional custom spec files mapping (initialized below)
SPEC_FILES = {}


class APISpecs(object):
    """ Represents the API specification document of an API. """

    def __init__(self, content):
        self.content = content

    def get_path_candidates(self):
        candidates = self.content.get('paths', {})
        candidates.update(self.content.get('x-ms-paths', {}))
        return candidates


class APITarget(object):
    """ Represents the API specification of a particular API method. """

    def __init__(self, method, path_pattern, method_details):
        self.method = method
        self.path_pattern = path_pattern
        self.method_details = method_details
        self.resource_type = None

    def __repr__(self):
        return 'APITarget(%s,%s)' % (self.method, self.path_pattern)


def get_api_specs_folder():
    path = os.path.join(config.TMP_FOLDER, 'azure-api-specs', 'azure-rest-api-specs-master')
    mkdir(path)
    return path


def load_api_spec(api):
    spec_file = SPECS.get(api)
    if not spec_file:
        log('Unable to find spec for API identifier "%s"' % api)
        return
    if isinstance(spec_file, dict):
        spec_file = next(iter(spec_file.values()))
    spec_file = os.path.join(get_api_specs_folder(), 'specification', spec_file)
    content = load_file(spec_file)
    if not content:
        raise Exception('Unable to load specifications for API "%s" from file: %s' % (api, spec_file))
    result = json.loads(content)
    return APISpecs(result)


def load_all_api_specs():
    result = {api: load_api_spec(api) for api in SPECS.keys()}
    return result


# TODO deprecated - remove?
def get_matching_spec(req, candidates):
    path_patterns = get_matching_paths(req.path_to_match, candidates.keys())
    if not path_patterns:
        log('Unable to find matching pattern: %s %s - %s' % (req.method, req.path_to_match, list(candidates.keys())))
        return
    for path_pattern in path_patterns:
        details = candidates[path_pattern]
        method_details = details.get(req.method.lower())
        if method_details:
            return APITarget(req.method, path_pattern, method_details)


def download_api_specs():
    root_dir = get_api_specs_folder()
    target_dir = os.path.realpath(os.path.join(root_dir, '..'))
    test_file = os.path.join(root_dir, 'package.json')
    if DOWNLOAD_FULL_SPECS and not os.path.exists(test_file):
        tmp_archive = os.path.join(target_dir, 'tmp.azure.specs.zip')
        download_and_extract_with_retry(SPEC_ZIP_URL, tmp_archive, target_dir)
        rm_rf(tmp_archive)

    test_file = os.path.join(root_dir, 'specification', 'eventgrid', 'resource-manager',
        'Microsoft.EventGrid', 'preview')
    if os.path.exists(test_file):
        for preview_folder in glob.glob('%s/**/preview/' % (target_dir), recursive=True):
            rm_rf(preview_folder)

    # download custom/preview files
    if not SPEC_FILES:
        for _, path in SPECS.items():
            branch = 'master'
            if isinstance(path, dict):
                branch, path = next(iter(path.items()))
            SPEC_FILES.update({path: GITHUB_AZURE_SPECS_URL.replace('<branch>', branch)})
    for key, base_url in SPEC_FILES.items():
        test_file = os.path.join(root_dir, 'specification', key)
        if not os.path.exists(test_file):
            url = '%s/specification/%s' % (base_url, key)
            download(url, test_file)
