import os
import logging
from localstack import config, constants
from localstack.utils.aws import aws_stack
from localstack.utils.common import start_worker_thread, short_uid, new_tmp_file, save_file
from localstack.services.install import download_and_extract_with_retry
from localstack_ext.utils.hadoop import start_hadoop_spark_container, run_in_spark, copy_into_spark_container

LOG = logging.getLogger(__name__)

AWS_GLUE_LIBS_URL = 'https://github.com/awslabs/aws-glue-libs/archive/refs/heads/glue-1.0.zip'
AWS_GLUE_LIBS_DIR = '/tmp/aws-glue-libs'
AWS_GLUE_JAVA_LIBS_URL = 'https://localstack-web-assets.s3.amazonaws.com/aws-glue-libs.zip'

JOB_RUNS = {}


def start_job_run(data):
    def _start(*args):
        install_libs()

        main_file = '/tmp/script-%s.scala' % short_uid()
        local_file = new_tmp_file()
        s3_client = aws_stack.connect_to_service('s3')
        script_loc = data.get('Command', {}).get('ScriptLocation')
        if not script_loc:
            LOG.warning('Unable to find ScriptLocation in job details: %s' % data)
            return
        bucket, _, key = script_loc.partition('://')[2].partition('/')
        LOG.debug('Attempting to download Glue job script file from S3 location: %s' % script_loc)
        s3_client.download_file(bucket, key, local_file)
        copy_into_spark_container(local_file, main_file)

        # TODO: the code below is a dirty hack, but just to get things working for now...
        default_args = data.get('DefaultArguments', {})
        repl_cmd = (r'\$intp.replScope.filter(x => x.tpe.toString == \"()type\" && !x.name.startsWith(\"res\"))' +
            r'.take(1).map(x => \$intp.interpret(x.name + \".main(Array())\"))')
        class_name = default_args.get('--class')
        if class_name:
            repl_cmd = '%s.main(Array())' % class_name
        cmd = ('bash -c \'echo "{repl}" | ' +
            'AWS_ACCESS_KEY_ID={akey} AWS_SECRET_ACCESS_KEY={skey} AWS_REGION={region} ' +
            'SPARK_CONF_DIR={basedir}/conf java -Dcom.amazonaws.sdk.disableCertChecking=true ' +
            '-cp {basedir}/conf/:/usr/local/spark-2.4.3-bin-without-hadoop-scala-2.12/jars/*:' +
            '{basedir}/jarsv1/* -Dscala.usejavacp=true -Xmx1g org.apache.spark.deploy.SparkSubmit ' +
            "--class org.apache.spark.repl.Main spark-shell -i {mainfile}'").format(
                region=aws_stack.get_region(), basedir=AWS_GLUE_LIBS_DIR, mainfile=main_file,
                repl=repl_cmd, akey=constants.TEST_AWS_ACCESS_KEY_ID, skey=constants.TEST_AWS_SECRET_ACCESS_KEY)

        LOG.debug('Running command for Glue job: %s' % cmd)
        result = run_in_spark(cmd)
        log_delimiter = 'SSL Certificate checking for endpoints has been explicitly disabled.'
        result = result.partition(log_delimiter)[2] or result

        LOG.debug('Received result for Glue job: %s' % result)
        JOB_RUNS[run_id]['result'] = result
        JOB_RUNS[run_id]['status'] = 'finished'

    run_id = short_uid()
    JOB_RUNS[run_id] = {'status': 'running'}
    start_worker_thread(_start)
    return run_id


def install_libs():
    thread = start_worker_thread(lambda *args: start_hadoop_spark_container())
    tmp_archive = os.path.join(config.TMP_FOLDER, 'aws-glue-libs.zip')
    local_dir = os.path.join(config.TMP_FOLDER, 'aws-glue-libs')
    local_root_dir = os.path.join(local_dir, 'aws-glue-libs-glue-1.0')
    download_and_extract_with_retry(AWS_GLUE_LIBS_URL, tmp_archive, local_dir)
    thread.join()
    jars_dir = '%s/jarsv1' % AWS_GLUE_LIBS_DIR

    try:
        run_in_spark('ls -la %s' % AWS_GLUE_LIBS_DIR, print_error=False)
    except Exception:
        copy_into_spark_container(local_root_dir, AWS_GLUE_LIBS_DIR)
        run_in_spark('sed -i "s/^mvn/# mvn/" %s/bin/glue-setup.sh' % AWS_GLUE_LIBS_DIR)
        run_in_spark(r"sed -i 's/mkdir \$/mkdir -p $/' %s/bin/glue-setup.sh" % AWS_GLUE_LIBS_DIR)
        content = ('spark.driver.extraClassPath {jars_dir}/*\n' +
            'spark.executor.extraClassPath {jars_dir}/*\n' +
            'spark.driver.allowMultipleContexts = true').format(jars_dir=jars_dir)
        local_file = new_tmp_file()
        save_file(local_file, content)
        run_in_spark('mkdir -p %s/conf' % AWS_GLUE_LIBS_DIR)
        copy_into_spark_container(local_file, '%s/conf/spark-defaults.conf' % AWS_GLUE_LIBS_DIR)

    try:
        run_in_spark('ls -la %s/aws-java-sdk-1.11.774.jar' % jars_dir, print_error=False)
    except Exception:
        LOG.debug('Copying missing JARs for Glue job execution into Docker container (this may take some time)')
        run_in_spark('mkdir -p %s' % jars_dir)
        tmp_archive = os.path.join(config.TMP_FOLDER, 'aws-glue-libs-java.zip')
        local_dir = os.path.join(config.TMP_FOLDER, 'aws-glue-libs-java')
        download_and_extract_with_retry(AWS_GLUE_JAVA_LIBS_URL, tmp_archive, local_dir)
        copy_into_spark_container(local_dir, jars_dir)
        run_in_spark("bash -c 'mv {jd}/aws-glue-libs-java/* {jd}/'".format(jd=jars_dir))
