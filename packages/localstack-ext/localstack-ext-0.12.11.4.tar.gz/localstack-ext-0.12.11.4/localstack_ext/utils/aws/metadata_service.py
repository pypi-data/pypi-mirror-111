import logging
from localstack.utils.common import start_thread, TMP_THREADS
from localstack.services.generic_proxy import GenericProxy, ProxyListener, serve_flask_app

LOG = logging.getLogger(__name__)

METADATA_SERVICE_PORT = 80
USE_FLASK = False


class MetadataServiceListener(ProxyListener):

    def forward_request(self, method, path, data, headers):
        LOG.debug('Instance metadata service request: %s %s %s' % (method, path, data))
        if path == '/latest/api/token':
            pass

        return 404


def start_metadata_service(port=None):
    port = port or METADATA_SERVICE_PORT
    LOG.info('Starting AWS instance metadata service on port %s' % port)
    if USE_FLASK:
        from metadataproxy import app
        return start_thread(lambda *args: serve_flask_app(app, port))
    proxy = GenericProxy(port, update_listener=MetadataServiceListener())
    proxy.start()
    TMP_THREADS.append(proxy)
    return proxy
