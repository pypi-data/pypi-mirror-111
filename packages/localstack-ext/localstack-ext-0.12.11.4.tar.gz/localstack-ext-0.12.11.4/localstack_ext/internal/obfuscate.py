import os
import glob
import shutil
import subprocess
from localstack.utils.common import mkdir, run

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_FOLDER = 'localstack_ext'


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def obfuscate():
    # obfuscate_opy()
    # obfuscate_pyarmor()
    obfuscate_pyminifier()
    # obfuscate_intensio()


def copy_target_code():
    root_dir = root_code_dir()
    source = root_dir
    target = os.path.realpath(os.path.join(root_dir, '..', 'build'))
    excluded = os.path.realpath(os.path.join(target, 'localstack_ext', 'internal'))
    mkdir(target)
    # copy target code
    cmd = 'cp -r "%s" "%s/"' % (source, target)
    run(cmd)
    # remove excluded code
    cmd = 'rm -r "%s"' % (excluded)
    run(cmd)
    return target


def obfuscate_intensio():
    root_dir = root_code_dir()
    source = root_dir
    target = os.path.realpath(os.path.join(root_dir, '..', 'build', ROOT_FOLDER))
    clone_cmd = ('(cd /tmp; test -e Intensio-Obfuscator || ' +
        'git clone https://github.com/Hnfull/Intensio-Obfuscator)')
    run(clone_cmd)

    cmd = '/tmp/Intensio-Obfuscator/intensio/intensio_obfuscator.py'
    cmd = ' '.join([cmd, '-i', source, '-o', target, '-m', 'lower', '-rts'])
    cmd = 'python3 %s' % cmd
    run(cmd)


def obfuscate_pyminifier():
    from pyminifier import pyminify
    target = copy_target_code()

    options = AttrDict({
        'pyz': False, 'prepend': False, 'outfile': None, 'destdir': None,
        'obfuscate': False, 'obf_classes': False, 'obf_functions': False,
        'obf_variables': False, 'obf_builtins': True, 'obf_import_methods': False,
        'use_nonlatin': False, 'nominify': False, 'tabs': False,
        'replacement_length': 5, 'bzip2': False, 'gzip': False
    })
    excluded = ('__init__.py', 'config.py', 'constants.py', 'cli.py')
    for dirpath, subdirs, files in os.walk(os.path.join(target, ROOT_FOLDER)):
        for f in files:
            if f in excluded or not f.endswith('.py'):
                continue
            full_path = os.path.join(dirpath, f)
            options['outfile'] = full_path
            pyminify(options, [full_path])


def obfuscate_pyarmor():
    import pyarmor
    root_dir = root_code_dir()
    source = os.path.join(root_dir, '__init__.py')
    target = os.path.realpath(os.path.join(root_dir, '..', 'build', ROOT_FOLDER))
    cmd = 'pyarmor obfuscate -r --output %s %s' % (target, source)
    subprocess.check_output(cmd, shell=True)

    # copy native libs for different platforms
    base_path = os.path.join(os.path.dirname(pyarmor.__file__), 'platforms')
    for platform in ('darwin64', 'linux64', 'windows64'):
        for lib_file in glob.glob('%s/%s/*' % (base_path, platform)):
            shutil.copy(lib_file, target)

    # copy plugins.py in plain text
    plugins_file = os.path.realpath(os.path.join(root_dir, 'plugins.py'))
    shutil.copy(plugins_file, os.path.join(target, 'plugins.py'))


def obfuscate_opy():
    from localstack_ext.internal.obfuscate import opy
    dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = root_code_dir()
    source = root_dir
    target = os.path.realpath(os.path.join(root_dir, '..', 'build', ROOT_FOLDER))
    config = os.path.realpath(os.path.join(dir, 'obfuscate.cfg'))
    main_file = opy.__file__
    cmd = ' '.join([main_file, source, target, config])
    result = subprocess.check_output('python %s' % cmd, shell=True)
    print(result.decode('utf-8'))


def root_code_dir():
    dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.realpath(os.path.join(dir, '..'))


if __name__ == '__main__':
    obfuscate()
