import os
import json
import logging
from localstack import config as localstack_config
from localstack.utils.common import (
    run, new_tmp_dir, save_file, wait_for_port_open, TMP_PROCESSES, start_thread, to_bytes, timestamp,
    get_free_tcp_port)
from localstack.services.infra import log_startup_message
from localstack.services.install import download_and_extract_with_retry
from localstack.utils.server.proxy_server import start_tcp_proxy
from localstack_ext.services.rds.db_utils import DBBackend, STATE, get_db_port_cache_key

LOG = logging.getLogger(__name__)

# TODO: update to version 3.4.11?
# TINKERPOP_SERVER = 'https://downloads.apache.org/tinkerpop/'
TINKERPOP_SERVER = 'https://archive.apache.org/dist/tinkerpop/'
TINKERPOP_DIR = 'apache-tinkerpop-gremlin-server-3.4.10'
TINKERPOP_URL = '%s/3.4.10/%s-bin.zip' % (TINKERPOP_SERVER, TINKERPOP_DIR)

GREMLIN_SERVER_CONF = """
host: 0.0.0.0
port: <port>
graphs:
  graph: <tinkergraph_conf>
serializers:
  - className: org.apache.tinkerpop.gremlin.driver.ser.GraphSONMessageSerializerV3d0
    config: { ioRegistries: [org.apache.tinkerpop.gremlin.tinkergraph.structure.TinkerIoRegistryV3d0] }
channelizer: org.apache.tinkerpop.gremlin.server.channel.WsAndHttpChannelizer
scriptEngines: {
  gremlin-groovy: {
    plugins: { org.apache.tinkerpop.gremlin.server.jsr223.GremlinServerGremlinPlugin: {},
               org.apache.tinkerpop.gremlin.tinkergraph.jsr223.TinkerGraphGremlinPlugin: {},
               org.apache.tinkerpop.gremlin.jsr223.ImportGremlinPlugin: {
                    classImports: [java.lang.Math], methodImports: [java.lang.Math#*]},
               org.apache.tinkerpop.gremlin.jsr223.ScriptFileGremlinPlugin: {files: [<groovy_init>]}}}}
metrics:
  slf4jReporter: {enabled: true, interval: 180000}
"""
TINKERGRAPH_PROPS = """
gremlin.graph=org.apache.tinkerpop.gremlin.tinkergraph.structure.TinkerGraph
gremlin.tinkergraph.vertexIdManager=ANY
"""
GROOVY_GRAPH_INIT = """
def globals = [:]
globals << [g : traversal().withEmbedded(graph).withStrategies(ReferenceElementStrategy)]
"""

# NOTE: Neptune API uses the same API as RDS - in fact, API requests contain "rds" in the auth header.
# Hence, we reuse the API methods from RDS and only add a specialized DBBackend for Graph DBs (Gremlin) below...


class DBBackendGremlin(DBBackend):
    ENGINES = ['neptune']

    def start_db_instance(self, req_data, region_name=None):
        install_graphdb()
        # start server
        port = req_data['Port']
        result = start_server(port)
        # store state
        cache_key = get_db_port_cache_key(req_data)
        STATE[cache_key] = result


def install_graphdb():
    target_dir = os.path.join(localstack_config.TMP_FOLDER, 'neptunedb')
    startup_script = os.path.join(target_dir, TINKERPOP_DIR, 'bin', 'gremlin-server.sh')
    if not os.path.exists(startup_script):
        LOG.debug('Downloading dependencies for Neptune Graph DB API (this may take some time) ...')
        tmp_archive = os.path.join(target_dir, 'neptunedb.zip')
        download_and_extract_with_retry(TINKERPOP_URL, tmp_archive, target_dir)
    return target_dir


def get_startup_script():
    target_dir = os.path.join(localstack_config.TMP_FOLDER, 'neptunedb')
    return os.path.join(target_dir, TINKERPOP_DIR, 'bin', 'gremlin-server.sh')


def start_server(port):
    backend_port = get_free_tcp_port()
    script = get_startup_script()
    config_dir = new_tmp_dir()
    gremlin_yml = os.path.join(config_dir, 'gremlin-server.yml')
    tinker_props = os.path.join(config_dir, 'tingergraph.properties')
    init_groovy = os.path.join(config_dir, 'init.groovy')
    server_conf = GREMLIN_SERVER_CONF.replace('<port>', str(backend_port))
    server_conf = server_conf.replace('<tinkergraph_conf>', tinker_props)
    server_conf = server_conf.replace('<groovy_init>', init_groovy)
    save_file(gremlin_yml, server_conf)
    save_file(tinker_props, TINKERGRAPH_PROPS)
    save_file(init_groovy, GROOVY_GRAPH_INIT)
    env_vars = {
        'GREMLIN_YAML': gremlin_yml,
        'PID_DIR': config_dir
    }
    LOG.info('Starting Neptune DB instance on port %s' % port)
    cmd = 'cd %s; exec %s %s' % (config_dir, script, gremlin_yml)
    process = run(cmd, asynchronous=True, env_vars=env_vars, outfile=os.devnull)
    TMP_PROCESSES.append(process)
    wait_for_port_open(backend_port, retries=13, sleep_time=2)
    state = STATE[port] = {}
    state['server'] = process
    state['start_time'] = start_time = timestamp()

    def handler(data):
        if data.startswith(b'GET /status'):
            result = get_status_response(start_time)
            return None, result
        return data, None
    proxy = start_thread(lambda *args, **kwargs: start_tcp_proxy(port, backend_port, handler, **kwargs))
    state['proxy'] = proxy

    return state


def get_status_response(start_time):
    # https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-status.html
    result = {
        'status': 'healthy',
        'startTime': start_time,
        'dbEngineVersion': 'development',
        'role': 'writer',
        'gremlin': {'version': 'tinkerpop-3.4.1'},
        'sparql': {'version': 'sparql-1.1'},
        'labMode': {
            'Streams': 'disabled',
            'ReadWriteConflictDetection': 'enabled'
        },
        'rollingBackTrxCount': '0'
    }
    payload = json.dumps(result)
    result = wrap_http_response_payload(payload)
    return to_bytes(result)


def wrap_http_response_payload(payload):
    result = 'HTTP/1.1 200 OK\r\n'
    result += 'Content-Type: application/json\r\n'
    result += 'Content-Length: %s\r\n' % len(payload)
    result += '\r\n'
    result += payload
    return result


def start_neptune(*args, **kwargs):
    # Only print startup message here, as we're reusing the RDS API...
    log_startup_message('Neptune')
