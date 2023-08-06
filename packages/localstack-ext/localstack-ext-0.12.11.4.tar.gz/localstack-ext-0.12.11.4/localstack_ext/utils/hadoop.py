import os
import re
import time
import logging
import prestodb
from pyhive import hive as pyhive_hive
from localstack import config as localstack_config
from localstack.utils.common import (
    retry, get_docker_container_names, save_file, run, new_tmp_file, rm_rf,
    wait_for_port_open, get_service_protocol, download, mkdir)
from localstack.services.awslambda.lambda_executors import get_main_endpoint_from_container
from localstack_ext import config as ext_config
from localstack_ext.utils.common import get_docker_container_host
from localstack_ext.services.awslambda import lambda_launcher

LOG = logging.getLogger(__name__)

# use a pseudo-random but static port here, as the bigdata container may survive LocalStack restarts
PORT_ATHENA_BACKEND = 41983

# TODO make configurable
SSH_PORT = 2122

SPARK_CONTAINER_NAME = 'localstack_spark'
SPARK_IMAGE_NAME = 'localstack/spark'
PRESTO_CONTAINER_NAME = 'localstack_presto'
PRESTO_IMAGE_NAME = 'localstack/presto'

USE_SINGLE_CONTAINER = True

if USE_SINGLE_CONTAINER:
    SPARK_CONTAINER_NAME = PRESTO_CONTAINER_NAME = 'localstack_bigdata'
    SPARK_IMAGE_NAME = PRESTO_IMAGE_NAME = 'localstack/bigdata'

PRESTO_USER_NAME = 'test'
PRESTO_CATALOG_NAME = 'hive'
PRESTO_SCHEMA = 'default'

HIVE_VERSION = '2.3.5'
HIVE_INITIALIZED = {}

HIVE_JAR_FILES = [
    # NOTE: adding additional JARs doesn't work easily, due to inconsistencies between different Hive versions
    # 'https://repo1.maven.org/maven2/org/keedio/openx/data/json/1.3.7.3/json-1.3.7.3.jar',
    # 'https://repo1.maven.org/maven2/org/keedio/openx/data/json-serde/1.3.7.3/json-serde-1.3.7.3.jar',
    # 'https://repo1.maven.org/maven2/org/apache/hive/hive-serde/1.2.2/hive-serde-1.2.2.jar',
]
HIVE_LIB_DIR = '/usr/local/apache-hive-<version>-bin/lib'

HIVE_SITE_XML = """
<configuration>
    <property>
        <name>hive.server2.thrift.bind.host</name>
        <value>0.0.0.0</value>
    </property>
    <property>
        <name>hive.server2.transport.mode</name>
        <value>binary</value>
    </property>
    <property>
        <name>hive.server2.thrift.port</name>
        <value>10000</value>
    </property>
    <property>
        <name>hive.metastore.uris</name>
        <value>thrift://localhost:9083</value>
    </property>
    <property>
        <name>hive.server2.enable.doAs</name>
        <value>false</value>
    </property>
    <property>
        <name>hive.server2.authentication</name>
        <value>NOSASL</value>
    </property>
    <property>
        <name>fs.s3.awsAccessKeyId</name>
        <value>test</value>
    </property>
    <property>
        <name>fs.s3.awsSecretAccessKey</name>
        <value>test</value>
    </property>
    <property>
        <name>fs.s3.endpoint</name>
        <value>{s3_endpoint}</value>
    </property>
    <property>
        <name>fs.s3.path.style.access</name>
        <value>true</value>
    </property>
    <property>
        <name>hive.s3.endpoint</name>
        <value>{s3_endpoint}</value>
    </property>
    <property>
        <name>fs.s3a.awsAccessKeyId</name>
        <value>test</value>
    </property>
    <property>
        <name>fs.s3a.awsSecretAccessKey</name>
        <value>test</value>
    </property>
    <property>
        <name>fs.s3a.access.key</name>
        <value>test</value>
    </property>
    <property>
        <name>fs.s3a.secret.key</name>
        <value>test</value>
    </property>
    <property>
        <name>fs.s3a.endpoint</name>
        <value>{s3_endpoint}</value>
    </property>
    <property>
        <name>fs.s3a.path.style.access</name>
        <value>true</value>
    </property>
    <property>
        <name>fs.s3n.awsAccessKeyId</name>
        <value>test</value>
    </property>
    <property>
        <name>fs.s3n.awsSecretAccessKey</name>
        <value>test</value>
    </property>
    <property>
        <name>fs.s3n.endpoint</name>
        <value>{s3_endpoint}</value>
    </property>
    <property>
        <name>fs.s3n.path.style.access</name>
        <value>true</value>
    </property>
</configuration>
"""

PRESTO_CONFIG = """
connector.name=hive-hadoop2
# hive.metastore=file
# hive.metastore.catalog.dir=file:///tmp/hive_catalog
# hive.metastore.user=test
hive.metastore.uri=thrift://{hive_host}
hive.s3.path-style-access=true
hive.s3.endpoint={s3_endpoint}
hive.s3.aws-access-key=test
hive.s3.aws-secret-key=test
hive.force-local-scheduling=true
hive.non-managed-table-creates-enabled=true
hive.non-managed-table-writes-enabled=true
hive.allow-drop-table=true
"""


def run_in_spark(cmd, print_error=True, flags=None):
    return run_in_container(cmd, SPARK_CONTAINER_NAME, print_error=print_error, flags=flags)


def run_in_presto(cmd, print_error=True, flags=None):
    return run_in_container(cmd, PRESTO_CONTAINER_NAME, print_error=print_error, flags=flags)


def run_in_container(cmd, container_name, print_error, flags=None):
    flags = flags or ''
    exec_cmd = '%s exec %s %s %s' % (localstack_config.DOCKER_CMD, flags, container_name, cmd)
    return run(exec_cmd, print_error=print_error)


def start_hadoop_spark_container(wait_for_hive=False):
    container_names = get_docker_container_names()

    # ensure that the container is running
    if SPARK_CONTAINER_NAME not in container_names:
        start_single_bigdata_container()

    # ensure that the process is running inside the container
    try:
        ps_cmd = 'ps aux | grep hiveserver2 | grep -v grep'
        run_in_spark('bash -c "%s"' % ps_cmd, print_error=False)
    except Exception:
        LOG.info('Starting Spark/Hadoop server in Docker container "%s"' % SPARK_CONTAINER_NAME)

        # start up local DNS server
        daemons_file = '/tmp/ls-daemons.py'
        try:
            run_in_spark('ls -la %s' % daemons_file, print_error=False)
        except Exception:
            local_daemons_file = new_tmp_file()
            endpoint_from_container = get_main_endpoint_from_container()
            save_file(local_daemons_file, lambda_launcher.DAEMON_SCRIPT)
            copy_into_container(local_daemons_file, SPARK_CONTAINER_NAME, daemons_file)
            LOG.debug('Starting up local DNS daemon script in bigdata container')
            run_in_spark('bash -c "nohup python {df} > {df}.log &"'.format(df=daemons_file),
                flags='-e LOCALSTACK_HOSTNAME=%s' % endpoint_from_container)

        # Set hive configuration
        hive_home = '/usr/local/apache-hive-%s-bin' % HIVE_VERSION
        site_xml = '%s/conf/hive-site.xml' % hive_home
        site_xml_local = new_tmp_file()
        s3_endpoint = 'http%s://%s:%s' % ('s' if localstack_config.USE_SSL else '',
            get_db_engine_hostname(), localstack_config.PORT_S3)
        hive_site_xml_content = HIVE_SITE_XML.format(s3_endpoint=s3_endpoint)
        save_file(site_xml_local, hive_site_xml_content)
        copy_into_container(site_xml_local, SPARK_CONTAINER_NAME, site_xml)

        # Make sure that libs for s3:// Hive locations are available
        lib1 = '/usr/local/hadoop-2.9.2/share/hadoop/tools/lib/aws-java-sdk-bundle-1.11.199.jar'
        lib2 = '/usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-aws-2.9.2.jar'
        cmd = 'cp %s %s %s/lib/' % (lib1, lib2, hive_home)
        run_in_spark(cmd)

        # Clean up any existing metadata and recreate schema db
        cmd = "bash -c 'rm -rf /metastore_db ; schematool -initSchema -dbType derby'"
        run_in_spark(cmd)

        # Start HDFS namenode in container
        log_file = '/tmp/hdfs-namenode.log'
        cmd = 'mkdir -p /tmp/hadoop-root/dfs/name; hdfs namenode -format'
        cmd = '%s; ps aux | grep namenode.NameNode | grep -v grep || nohup hdfs namenode' % cmd
        cmd = "bash -c '%s > %s 2>&1 &'" % (cmd, log_file)
        run_in_spark(cmd)
        time.sleep(5)

        # Start Hive metastore in container
        log_file = '/tmp/hive-metastore.log'
        cmd = "bash -c 'nohup hive --service metastore > %s 2>&1 &'" % log_file
        run_in_spark(cmd)
        time.sleep(6)

        # Start Hive server in container
        env_string = 'HIVE_SERVER2_THRIFT_BIND_HOST=0.0.0.0 HIVE_SERVER2_THRIFT_PORT=10000'
        log_file = '/tmp/hiveserver2.log'
        cmd = "bash -c '%s nohup hiveserver2 > %s 2>&1 &'" % (env_string, log_file)
        run_in_spark(cmd)
        time.sleep(4)
        LOG.debug('Done starting Spark/Hadoop server in Docker container "%s"' % SPARK_CONTAINER_NAME)

    if wait_for_hive and not HIVE_INITIALIZED:
        def check_hive(*args):
            try:
                execute_hive_query('show tables', skip_start=True)
                # create HDFS base dir
                run_in_spark('hdfs dfs -mkdir -p /user/hive/warehouse')
                HIVE_INITIALIZED['done'] = True
            except Exception:
                LOG.debug('Unable to get Hive status, probably still starting up - retrying...')
                raise
        # poll for startup success - note that this can take a very long time
        retry(check_hive, retries=15, sleep=7)


def start_single_bigdata_container():
    container_names = get_docker_container_names()
    if SPARK_CONTAINER_NAME in container_names:
        return

    LOG.info('Starting Athena/EMR Docker container "%s" (this may take a while ...)' % PRESTO_CONTAINER_NAME)
    presto_port = PORT_ATHENA_BACKEND
    docker_cmd = localstack_config.DOCKER_CMD
    sleep_cmd = 'bash -c "while [ 1 ]; do sleep 999; done"'
    ports_flags = '-p {ssh}:{ssh} -p {hv}:{hv} -p {mt}:{mt} -p {pr}:{pr} -p {sm}:{sm} -p {sui}:{sui}'.format(
        ssh=SSH_PORT, hv=ext_config.PORT_HIVE_SERVER, mt=ext_config.PORT_HIVE_METASTORE,
        pr=presto_port, sm=ext_config.PORT_SPARK_MASTER, sui=ext_config.PORT_SPARK_UI)
    dns_flag = '--dns 127.0.0.1' if use_custom_dns() else ''
    cmd = '%s create -it --rm -e PRESTO_PORT=%s %s %s %s --name %s %s %s' % (
        docker_cmd, presto_port, ports_flags, dns_flag, ext_config.BIGDATA_DOCKER_FLAGS,
        SPARK_CONTAINER_NAME, SPARK_IMAGE_NAME, sleep_cmd)
    container_id = run(cmd).strip().split('\n')[-1]
    run('%s start "%s"' % (docker_cmd, container_id))
    time.sleep(5)

    # add additional libraries to container
    download_additional_libs(container_id)


def download_additional_libs(container_id):
    """ Download additional libraries for the container.
        Note: temporary fix, libs should probably get baked into the image. """
    jar_dir = os.path.join(localstack_config.TMP_FOLDER, 'hive-jars')
    mkdir(jar_dir)
    target_dir = HIVE_LIB_DIR.replace('<version>', HIVE_VERSION)
    for jar_url in HIVE_JAR_FILES:
        jar_local = os.path.join(jar_dir, jar_url.rpartition('/')[2])
        download(jar_url, jar_local)
        copy_into_container(jar_local, container_id, target_dir)


def start_presto_container(wait=False):
    container_names = get_docker_container_names()
    port = PORT_ATHENA_BACKEND
    host_from_container = localstack_config.DOCKER_HOST_FROM_CONTAINER
    docker_cmd = localstack_config.DOCKER_CMD

    # ensure that the container is running
    if USE_SINGLE_CONTAINER or PRESTO_CONTAINER_NAME not in container_names:
        config_file = new_tmp_file()
        s3_endpoint = '%s://%s:%s' % (get_service_protocol(), host_from_container, localstack_config.PORT_S3)
        hive_host = '%s:%s' % (get_hive_host_from_presto(), ext_config.PORT_HIVE_METASTORE)
        presto_config = PRESTO_CONFIG.format(s3_endpoint=s3_endpoint, hive_host=hive_host, presto_port=port)
        save_file(config_file, presto_config)
        config_file_docker = '/etc/presto/catalog/hive.properties'
        if USE_SINGLE_CONTAINER:
            start_single_bigdata_container()
            copy_into_container(config_file, PRESTO_CONTAINER_NAME, config_file_docker)
            run_in_presto('sed -i s/8080/%s/g /etc/presto/config.properties' % port)
        else:
            cmd = '%s create --rm -p %s:%s -e PRESTO_PORT=%s --name %s %s' % (
                docker_cmd, port, port, port, PRESTO_CONTAINER_NAME, PRESTO_IMAGE_NAME)
            container_id = run(cmd).strip()
            copy_into_container(config_file, container_id, config_file_docker)
            run('%s start "%s"' % (docker_cmd, container_id))
            time.sleep(3)
        rm_rf(config_file)

    # ensure that the process is running inside the container
    try:
        ps_cmd = 'ps aux | grep prestosql.server | grep -v grep'
        run_in_presto("bash -c '%s'" % ps_cmd, print_error=False)
    except Exception:
        LOG.info('Starting Presto server in Docker container "%s"' % PRESTO_CONTAINER_NAME)
        start_cmd = 'nohup /usr/lib/presto/bin/launcher run 2>&1 >> /tmp/presto.log &'
        run_in_presto("bash -c '%s'" % start_cmd)

    athena_url = 'http://%s:%s' % (get_db_engine_hostname(), port)
    if wait:
        wait_for_port_open(athena_url)


def copy_into_container(local_path, container_id, target_path):
    return run('%s cp "%s" "%s:%s"' % (localstack_config.DOCKER_CMD, local_path, container_id, target_path))


def copy_into_spark_container(local_path, target_path):
    return copy_into_container(local_path, SPARK_CONTAINER_NAME, target_path)


def execute_presto_query(query):
    def do_run():
        start_presto_container(wait=True)
        host = get_db_engine_hostname()
        conn = prestodb.dbapi.connect(
            host=host, schema=PRESTO_SCHEMA, port=PORT_ATHENA_BACKEND,
            user=PRESTO_USER_NAME, catalog=PRESTO_CATALOG_NAME)
        cur = conn.cursor()
        cur.execute(query)
        rows = list(cur.fetchall())
        columns = [list(desc[:2]) for desc in cur.description]
        return {'rows': rows, 'columns': columns}

    retries = 10
    error = None
    for i in range(retries):
        try:
            return do_run()
        except Exception as e:
            error = e
            if 'Presto server is still initializing' in str(e):
                LOG.info('Presto server is still initializing, retrying in a few seconds...')
                continue
            else:
                break
    raise Exception('Unable to get result from Presto server after %s retries: %s' % (retries, error))


def prepare_hive_query(query):
    # strip trailing semicolon
    query = query.rstrip(' ;')

    # Athena uses older/deprecated versions of Hive libs which are incompatible with our Hive version
    query = re.sub(r'org\s*\.\s*openx\s*\.\s*data\s*\.\s*jsonserde\s*\.\s*JsonSerDe',
        'org.apache.hive.hcatalog.data.JsonSerDe', query)

    return query


def execute_hive_query(query, skip_start=False):
    if not skip_start:
        start_hadoop_spark_container(wait_for_hive=True)

    # prepare the query for execution
    query = prepare_hive_query(query)

    kwargs = {
        'auth': 'NOSASL'
    }
    conn = pyhive_hive.connect(get_db_engine_hostname(), ext_config.PORT_HIVE_SERVER, **kwargs)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except Exception as e:
        if 'already exists' not in str(e):
            raise
    if not cursor.description:
        return {'rows': [], 'columns': []}
    columns = [desc[:2] for desc in cursor.description]

    try:
        rows = list(cursor.fetchall())
    except Exception:
        rows = []

    LOG.debug('Hive query result: %s' % rows)
    return {'rows': rows, 'columns': columns}


def use_custom_dns():
    # TODO create custom config flag to disable DNS for Glue/Athena..?
    return ext_config.use_custom_dns()


def get_hive_host_from_presto():
    host_from_container = localstack_config.DOCKER_HOST_FROM_CONTAINER
    return 'localhost' if USE_SINGLE_CONTAINER else host_from_container


def get_db_engine_hostname():
    return get_docker_container_host()
