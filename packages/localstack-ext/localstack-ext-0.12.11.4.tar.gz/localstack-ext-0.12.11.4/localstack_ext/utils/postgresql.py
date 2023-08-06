import os
import time
import signal
import logging
import tempfile
import threading
import subprocess
import pg8000
from glob import glob
from contextlib import closing
from six.moves.queue import Queue
from postgresql_proxy import proxy, config_schema
from testing.common.database import (
    Database, DatabaseFactory, get_path_of, SkipIfNotInstalledDecorator)
from localstack.constants import LOCALHOST
from localstack.utils.common import (
    TMP_THREADS, load_file, save_file, to_str, is_root, new_tmp_file,
    chown_r, chmod_r, FuncThread, in_docker, run_safe)

__all__ = ['Postgresql', 'skipIfNotFound']

DEV_NULL = '/dev/null'

LOG = logging.getLogger(__name__)

SEARCH_PATHS = (['/usr/local/pgsql', '/usr/local'] +
                glob('/usr/pgsql-*') +  # for CentOS/RHEL
                glob('/usr/lib/postgresql/*') +  # for Debian/Ubuntu
                glob('/opt/local/lib/postgresql*'))  # for MacPorts

EXEC_USERNAME = 'localstack'
DEFAULT_DATABASE = 'test'
POSTGRES_CMDLINE_ARGS = '-h 0.0.0.0 -F -c logging_collector=off'


class Postgresql(Database):
    DEFAULT_SETTINGS = dict(auto_start=2,
                            base_dir=None,
                            initdb_args='-U postgres -A trust',
                            postgres_args=POSTGRES_CMDLINE_ARGS,
                            pid=None,
                            port=None,
                            copy_data_from=None)
    SETTINGS_INITIALIZED = False
    subdirectories = ['data', 'tmp']

    def __init__(self, *args, **kwargs):
        if not Postgresql.SETTINGS_INITIALIZED:
            if in_docker():
                # load timescaledb libs only if we're running in Docker
                self.DEFAULT_SETTINGS['postgres_args'] += ' -c shared_preload_libraries=timescaledb'
            Postgresql.SETTINGS_INITIALIZED = True
        super(Postgresql, self).__init__(*args, **kwargs)

    def initialize(self):
        self.custom_parameters = {}
        self.initdb = self.settings.pop('initdb', None) or find_program('initdb', ['bin'])
        self.postgres = self.settings.pop('postgres', None) or find_program('postgres', ['bin'])
        self.pg_ctl = self.settings.pop('pg_ctl', None) or find_program('pg_ctl', ['bin'])
        self.pg_dump = self.settings.pop('pg_dump', None) or find_program('pg_dump', ['bin'])
        self.pg_restore = self.settings.pop('pg_restore', None) or find_program('pg_restore', ['bin'])
        # Note: make sure the domain socket is created in a local tmp folder inside the
        # container, and NOT in any of the mounted directories, as this can cause startup errors
        # domain_socket_folder = os.path.join(self.base_dir, 'tmp')
        self.domain_socket_folder = tempfile.mkdtemp()

    def dsn(self, **kwargs):
        # "database=test host=localhost user=postgres"
        params = dict(kwargs)
        params.setdefault('port', self.settings['port'])
        params.setdefault('host', LOCALHOST)
        params.setdefault('user', 'postgres')
        params.setdefault('database', DEFAULT_DATABASE)
        return params

    def url(self, **kwargs):
        params = self.dsn(**kwargs)
        url = ('postgresql://%s@%s:%d/%s' %
               (params['user'], params['host'], params['port'], params['database']))
        return url

    def get_data_directory(self):
        return os.path.join(self.base_dir, 'data')

    def initialize_database(self):
        if is_root():
            exec_username = self.get_exec_username()
            chown_r(self.base_dir, exec_username)
            chown_r(self.domain_socket_folder, exec_username)
            try:
                chmod_r(DEV_NULL, 0o777)  # required, as in some cases we're getting "access denied" errors
            except Exception:
                pass

        if not os.path.exists(os.path.join(self.get_data_directory(), 'PG_VERSION')):
            args = ([self.initdb, '-D', self.get_data_directory(), '--lc-messages=C'] +
                    self.settings['initdb_args'].split())

            try:
                self.run_cmd(args)

                # configure pg_hba.conf
                conf_file = os.path.join(self.base_dir, 'data', 'pg_hba.conf')
                content = load_file(conf_file)
                content = '%s\nhost    all    all    0.0.0.0/0    md5' % content
                save_file(conf_file, content)
            except OSError as exc:
                raise RuntimeError('Failed to spawn initdb: %s' % exc)

    def run_cmd(self, args):
        args = self.prepend_su(args)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        if p.returncode != 0:
            raise RuntimeError('Command failed: %r' % err)
        return output

    def get_server_commandline(self):
        args = ([self.postgres,
                 '-p', str(self.settings['port']),
                 '-D', self.get_data_directory(),
                 '-k', self.domain_socket_folder] +
                self.settings['postgres_args'].split())
        return self.prepend_su(args)

    def dump_db(self, output_file=None, **kwargs):
        output_file = output_file or new_tmp_file()
        self._base_cmd(self.pg_dump, '-Fc', '-f', output_file, self.settings['database'])
        return output_file

    def restore_db(self, dump_file, **kwargs):
        self._base_cmd(self.pg_restore, '-d', self.settings['database'], dump_file)
        return

    def start(self, start_func=None):
        start_func = start_func or super(Postgresql, self).start
        self_ref = self
        queue = Queue()

        class DBThread(threading.Thread):
            def run(self):
                try:
                    start_func()
                    queue.put(0)
                except Exception as e:
                    LOG.info('Unable to start RDS Postgres DB thread: %s' % e)
                    queue.put(e)

            def stop(self, **kwargs):
                self_ref.stop()

        t = DBThread()
        t.start()
        result = queue.get()
        TMP_THREADS.append(t)
        if isinstance(result, Exception):
            raise result

    def restart(self):
        def startup():
            command = self.get_server_commandline()
            logger = open(os.path.join(self.base_dir, '%s.log' % self.name), 'wt')
            self.child_process = subprocess.Popen(command, stdout=logger, stderr=logger)

        LOG.debug('Restarting Postgresql instance %s' % self.base_dir)
        self.terminate()
        self.start(start_func=startup)

    def poststart(self):
        params = self.settings
        # create master superuser
        try:
            self.run_admin_query("CREATE USER \"%s\" WITH ENCRYPTED PASSWORD '%s'" % (
                params['user'], params['password']))
        except Exception as e:
            if 'already exists' in str(e):
                # looks like we're restoring DB state from an existing database -> return
                return
            raise
        self.run_admin_query('ALTER USER \"%s\" WITH SUPERUSER' % params['user'])
        # create rds_superuser and rds_replication roles
        run_safe(lambda: self.run_admin_query('CREATE ROLE rds_superuser'))
        run_safe(lambda: self.run_admin_query('CREATE ROLE rds_replication'))
        self.run_admin_query('ALTER ROLE \"rds_superuser\" WITH SUPERUSER')
        self.run_admin_query('ALTER ROLE \"rds_replication\" WITH SUPERUSER')
        # create default database and grant privileges
        db = params.get('database') or DEFAULT_DATABASE
        db and self.create_database(db)

    def run_admin_query(self, query):
        return self.run_query(query, admin=True)

    def run_query(self, query, *args, database=None, admin=False):
        connection = self.connect(database, admin=admin)
        with closing(connection) as conn:
            conn.autocommit = True
            with closing(conn.cursor()) as cursor:
                return cursor.execute(query, args)

    def connect(self, database=None, admin=False):
        database = database or self.settings.get('database')
        dsn = self.dsn(database=database, user=self.settings['user'], password=self.settings['password'])
        if admin:
            dsn = self.dsn(database='postgres')
        return pg8000.connect(**dsn)

    def list_databases(self):
        result = self.run_admin_query('SELECT datname FROM pg_database')
        result = [entry[0] for entry in result]
        excluded = ['postgres', 'template1', 'template0']
        result = [db for db in result if db not in excluded]
        return result

    def create_database(self, db):
        params = self.settings
        self.run_admin_query('CREATE DATABASE \"%s\"' % db)
        self.run_admin_query('GRANT ALL PRIVILEGES ON DATABASE \"%s\" TO \"%s\"' % (db, params['user']))
        self.run_admin_query('GRANT ALL PRIVILEGES ON DATABASE \"%s\" TO \"rds_superuser\"' % db)
        self.run_admin_query('GRANT ALL PRIVILEGES ON DATABASE \"%s\" TO \"rds_replication\"' % db)

    def apply_parameters(self, params):
        for param in params or []:
            self.custom_parameters[param['ParameterName']] = param
            name = param['ParameterName']
            value = param['ParameterValue']
            # map specific RDS parameters to DB parameters
            if name == 'rds.logical_replication':
                name = 'wal_level'
                value = 'logical' if value in ['1', 1] else 'replica'
            # run query to update system parameter
            query = "ALTER SYSTEM SET %s='%s'" % (name, value)
            LOG.debug('Running Postgresql system update: %s' % query)
            self.run_admin_query(query)

        # restart instance to apply settings
        self.restart()

    def is_server_available(self):
        try:
            with closing(pg8000.connect(**self.dsn(database='template1'))):
                pass
        except pg8000.Error:
            return False
        return True

    def terminate(self, *args):
        # send SIGINT instead of SIGTERM
        super(Postgresql, self).terminate(signal.SIGINT if os.name != 'nt' else None)

    def get_exec_username(self):
        try:
            exec_username = to_str(subprocess.check_output('whoami', shell=True)).strip()
            return exec_username if exec_username != 'root' else EXEC_USERNAME
        except Exception:
            return EXEC_USERNAME

    def prepend_su(self, cmd_args):
        if not is_root():
            return cmd_args
        exec_username = self.get_exec_username()
        return ['/bin/su', exec_username, '-c', ' '.join(cmd_args)]

    def _base_cmd(self, cmd, *args, **kwargs):
        params = dict(self.settings)
        params.update(kwargs)
        env = {'PGPASSWORD': params['password']}
        args = ['-p', str(params['port']),
                '-h', str(params.get('host') or LOCALHOST),
                '-U', str(params['user'])] + list(args)
        args = [cmd] + args
        return subprocess.check_output(args, env=env)


class PostgresqlFactory(DatabaseFactory):
    target_class = Postgresql


class PostgresqlSkipIfNotInstalledDecorator(SkipIfNotInstalledDecorator):
    name = 'PostgreSQL'

    def search_server(self):
        find_program('postgres', ['bin'])


skipIfNotFound = skipIfNotInstalled = PostgresqlSkipIfNotInstalledDecorator()


def find_program(name, subdirs):
    path = get_path_of(name)
    if path:
        return path

    for base_dir in SEARCH_PATHS:
        for subdir in subdirs:
            path = os.path.join(base_dir, subdir, name)
            if os.path.exists(path):
                return path

    raise RuntimeError('Command not found: %s' % name)


def start_postgres_proxy(port, backend_port, query_rewrite_handler):
    bind_host = '0.0.0.0'
    instance = {
        'listen': {
            'name': 'proxy',
            'host': bind_host,
            'port': port
        }, 'redirect': {
            'name': 'postgresql',
            'host': bind_host,
            'port': backend_port
        },
        'intercept': {
            'commands': {
                'queries': [{
                    'plugin': 'psql_interceptor',
                    'function': 'rewrite_query'
                }]
            },
            'responses': {}
        }
    }
    config = config_schema.Config({'instances': [instance]})

    plugins = {
        'psql_interceptor': query_rewrite_handler
    }

    class ProxyThread(FuncThread):

        def __init__(self, params={}):
            FuncThread.__init__(self, self.run_cmd, params)

        def run_cmd(self, *args):
            try:
                LOG.info('Starting PostgreSQL query listener/rewriter on port %s->%s' % (port, backend_port))
                self.psql_proxy = proxy.Proxy(config.instances[0], plugins)
                self.psql_proxy.listen()
            except Exception as e:
                LOG.info('Error running RDS proxy listener for ports %s->%s: %s' % (port, backend_port, e))

        def stop(self, *args, **kwargs):
            self.psql_proxy.stop()
            time.sleep(1)  # proxy takes some time to shut down ...

    thread = ProxyThread()
    thread.start()
    TMP_THREADS.append(thread)
    time.sleep(1)
    return thread
