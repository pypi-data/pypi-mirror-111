import os
import logging
import traceback
from localstack import config
from localstack.utils.common import to_str, to_bytes, run, mkdir
from localstack.services.generic_proxy import start_proxy_server, ProxyListener
from localstack_ext import config as ext_config
from localstack_ext.services.azure import api_specs
from localstack_ext.services.azure.routing import (
    determine_api, RequestContext, prepare_path_to_match, load_api_spec_for_request)
from localstack_ext.services.azure.azure_utils import log
from localstack_ext.services.azure.api_handlers import APIHandler

LOG = logging.getLogger(__name__)

HEADERS_CT_XML = {'content-type': 'text/xml'}
HEADERS_CT_JSON = {'content-type': 'application/json'}


class ProxyListenerAzure(ProxyListener):

    def forward_request(self, method, path, data, headers):
        result = None
        try:
            data_logged = '_binary_'
            try:
                data_logged = to_str(data or '')[:100] + ' ...'
            except Exception:
                pass
            api = determine_api(method, path, headers)
            print('AZURE ->REQ', api, method, path, data_logged)  # TODO: use logger
            req_ctx = RequestContext(method, path, data, headers, api)
            result = self.handle_request(req_ctx)
        except Exception as e:
            log('Error handling request: %s %s' % (e, traceback.format_exc()))
        if result is None:
            return 400
        return result

    def return_response(self, method, path, data, headers, response):
        content = to_str(response.content or '')
        if 'content-type' not in response.headers:
            if content.startswith('<'):
                response.headers.update(HEADERS_CT_XML)
            elif content.startswith('{') or content.startswith('['):
                response.headers.update(HEADERS_CT_JSON)
        content_logged = content[:100] + ' ...'
        print('AZURE RES->', response.status_code, method, path, content_logged, response.headers)  # TODO: use logger

    def handle_request(self, req):
        # apply customizations
        prepare_path_to_match(req)

        # see if we can find an API spec for this request
        load_api_spec_for_request(req)
        # if not req.spec:
        #     log('Unable to find API specs for request: %s %s %s' % (req.method, req.path, req.path_params))

        # find matching handler
        handler = APIHandler.get(req.api)
        if not handler:
            if not req.spec:
                log('Unable to find API handler "%s" for request: %s %s' % (req.api, req.method, req.path))
                return 404
            handler = APIHandler.get()

        # handle the request
        result = handler.handle_request(req)
        if result is None:
            return 200
        return result


# instantiate listener
UPDATE_AZURE = ProxyListenerAzure()


def install_components():
    install_dir = os.path.join(config.TMP_FOLDER, 'azure-functions')
    if not os.path.exists(os.path.join(install_dir, 'node_modules')):
        LOG.debug('Downloading and installing dependencies for Azure Functions')
        mkdir(install_dir)
        run('cd "%s"; npm i azure-functions-core-tools@3 --unsafe-perm true' % install_dir)


def start_amqp_broker():
    # TODO - terrible hacks below - work in progress!!
    return

    import os
    from localstack import config
    from localstack.utils.common import ShellCommandThread, TMP_THREADS
    print('!!!!start_amqp_broker')
    binary = os.path.join(config.TMP_FOLDER, 'dispatchd.alpine')
    # docker run --rm -it -p 5672:5672 -p 15672:15672 localstack/rabbitmq

    # TODO
    admin_port = 4510
    amqp_port = 4511
    persist_dir = '/tmp'
    cmd = 'STATIC_PATH=/static %s -admin-port %s -amqp-port %s -persist-dir %s' % (
        binary, admin_port, amqp_port, persist_dir)
    print(cmd)
    t = ShellCommandThread(cmd)
    t.start()
    TMP_THREADS.append(t)
    print('!!!!start_amqp_broker done')

    # TODO
    cmd = 'docker run --rm -it -p 5672:5672 -p 15672:15672 bitnami/rabbitmq'

    async def channel(self, reader, writer, stat_bytes, stat_conn):
        try:
            stat_conn(1)
            from localstack_ext.services.azure import azure_utils
            stepper, is_outgoing = azure_utils.SASLHandshake.get(self)
            handshake_done = False
            first_message = True

            while not reader.at_eof() and not writer.is_closing():
                data = await reader.read(65536)
                if not data:
                    break
                if stat_bytes is None:
                    continue
                stat_bytes(len(data))

                # patched the code below
                print('!!DATA!!', data)
                # import amqp
                # msg = amqp.
                if is_real_target:
                    data = data.replace(b'test.localhost.localstack.cloud', to_bytes(target.split(':')[0]))
                print('!!proxy data:', 'OUT' if is_outgoing else 'IN', len(data), data)
                direction = 'OUT' if is_outgoing else 'IN'
                if not is_real_target and not handshake_done and data.startswith(b'AMQP'):
                    steps = stepper.steps(is_outgoing)
                    print('!!STEPPER START', direction)
                    async for step in steps:
                        print('!!STEPPER step', direction, step)
                        if first_message or not is_outgoing:
                            first_message = False
                            writer.write(step)
                            await writer.drain()
                    handshake_done = True
                    continue

                # print('!!FORWARD data', direction, data)
                writer.write(data)
                await writer.drain()
        except Exception:
            pass
        finally:
            stat_conn(-1)
            writer.close()

    import pproxy.proto
    pproxy.proto.BaseProtocol.channel = channel

    # amqp_port = 5672
    # amqp_admin_port = 15672
    from localstack.utils.server import ssl_proxy
    target_host = 'localhost'
    target = '%s:%s' % (target_host, amqp_port)
    target = '%s:5672' % config.DOCKER_BRIDGE_IP
    target = 'tmp-bus1.servicebus.windows.net:5671'
    is_real_target = 'windows.net' in target
    print(target)
    ssl_proxy.start_ssl_proxy(5671, target, target_ssl=is_real_target)


def start_azure(port=None, asynchronous=False, update_listener=None):
    if not port:
        port = ext_config.PORT_AZURE

    api_specs.download_api_specs()
    if False:  # TODO
        install_components()

    # start additional components
    start_amqp_broker()

    print('Starting mock Azure APIs (port %s)' % port)
    proxy = start_proxy_server(port, update_listener=UPDATE_AZURE, use_ssl=True)
    return proxy
