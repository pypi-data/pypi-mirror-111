import re
import json
import logging
from localstack import config as localstack_config
from localstack.utils import bootstrap
from localstack.utils.aws import aws_stack
from localstack.utils.common import to_str, run, new_tmp_file, short_uid, rm_rf, clone
from localstack.utils.analytics import event_publisher
from localstack.services.generic_proxy import ProxyListener
from localstack_ext.utils.hadoop import SPARK_CONTAINER_NAME, start_hadoop_spark_container

LOG = logging.getLogger(__name__)

EVENT_EMR_CREATE_CLUSTER = 'emr.cc'
EVENT_EMR_DELETE_CLUSTER = 'emr.dc'

ACTION_PREFIX = 'ElasticMapReduce.'

# global state object
STATE = {}


class Step(object):
    def run(self, step, cluster):
        raise NotImplementedError()

    @classmethod
    def get_step(cls, step):
        options = step.get('HadoopJarStep', {})
        jar = options.get('Jar', '')
        if jar == 'command-runner.jar':
            return SparkAppStep()
        if jar.startswith('s3://'):
            return CustomJarStep()
        LOG.warning('Unable to run unknown step type for EMR cluster: %s' % step)

    def args_str(self, step):
        args = step['HadoopJarStep'].get('Args') or []
        return '"%s"' % '" "'.join(args)

    def copy_s3_file(self, url):
        """ Copy file from S3 bucket into container """
        client = aws_stack.connect_to_service('s3')
        bucket, _, key = url.replace('s3://', '').partition('/')
        match = re.match(r'.*/?[^/]+\.([^\.]+)', key)
        extension = '.%s' % match.group(1) if match else ''
        local_file = new_tmp_file()
        LOG.debug('Downloading S3 file for EMR job: bucket "%s", key "%s", local file "%s"' % (bucket, key, local_file))
        client.download_file(bucket, key, local_file)
        container_file = '/tmp/%s%s' % (short_uid(), extension)
        run('docker cp %s %s:%s' % (local_file, SPARK_CONTAINER_NAME, container_file))
        rm_rf(local_file)
        return container_file

    def run_command(self, cmd):
        # construct command and environment
        host_from_container = localstack_config.DOCKER_HOST_FROM_CONTAINER
        env_vars = {
            'AWS_REGION': aws_stack.get_region(),
            'AWS_ACCESS_KEY_ID': 'test',
            'AWS_SECRET_ACCESS_KEY': 'test'
        }
        for api in bootstrap.canonicalize_api_names():
            env_name = 'TEST_%s_URL' % api.upper()
            env_vars[env_name] = localstack_config.external_service_url(api, host_from_container)
        env_vars = ['-e %s="%s"' % (k, v) for k, v in env_vars.items()]
        env_vars = ' '.join(env_vars)
        command = 'docker exec %s %s %s' % (env_vars, SPARK_CONTAINER_NAME, cmd)

        # run command in container
        LOG.info('EMR job - running command: %s' % command)
        logs = run(command)
        return logs


class SparkAppStep(Step):
    def run(self, step, cluster):
        # copy JAR file args from S3 source into container
        step = clone(step)
        args = step['HadoopJarStep'].get('Args') or []
        tmp_files = []
        for i in range(len(args)):
            if args[i].startswith('s3://'):
                container_file = self.copy_s3_file(args[i])
                args[i] = container_file
                tmp_files.append(container_file)

        # construct command and run it in the container
        command = self.args_str(step)
        logs = self.run_command(command)

        # cleanup files in container
        if tmp_files:
            run('docker exec %s rm -f %s' % (SPARK_CONTAINER_NAME, ' '.join(tmp_files)))

        return logs


class CustomJarStep(Step):
    def run(self, step, cluster):
        details = step['HadoopJarStep']
        jar = details['Jar']
        args = self.args_str(step)

        # copy JAR file from S3 source into container
        container_file = self.copy_s3_file(jar)

        # construct command and run it in the container
        command = 'yarn jar %s %s' % (container_file, args)
        logs = self.run_command(command)

        # cleanup JAR in container
        run('docker exec %s rm -f %s' % (SPARK_CONTAINER_NAME, container_file))

        return logs


class ProxyListenerEMR(ProxyListener):

    # def forward_request(self, method, path, data, headers):
    #     action = headers.get('X-Amz-Target')
    #     print('EMR: %s' % action)
    #
    #     return True

    def return_response(self, method, path, data, headers, response):
        action = headers.get('X-Amz-Target')

        if action == '%sRunJobFlow' % ACTION_PREFIX:
            data = json.loads(to_str(data))
            event_publisher.fire_event(EVENT_EMR_CREATE_CLUSTER,
                payload={'d': event_publisher.get_hash(data.get('Name'))})
            self.startup_cluster(data, response)
        elif action == '%sAddJobFlowSteps' % ACTION_PREFIX:
            data = json.loads(to_str(data))
            self.add_flow_steps(data.get('Steps'))

    # ------------
    # API METHODS
    # ------------

    def startup_cluster(self, data, response):
        start_hadoop_spark_container()
        # run initialization steps
        self._run_steps(data)

    def add_flow_steps(self, steps):
        cluster = {}  # TODO
        self._run_steps(cluster, steps=steps)

    def _run_steps(self, cluster, steps=None):
        steps = steps or cluster.get('Steps', [])
        for step in steps:
            step_obj = Step.get_step(step)
            step_obj.run(step, cluster)


# instantiate listener
UPDATE_EMR = ProxyListenerEMR()
