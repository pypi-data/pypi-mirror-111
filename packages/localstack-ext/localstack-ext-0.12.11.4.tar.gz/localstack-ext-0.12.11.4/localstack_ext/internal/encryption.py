import json
import os
import sys
import glob
import pyaes
from localstack.utils.common import load_file, save_file, to_bytes
from localstack_ext.config import PROTECTED_FOLDERS, ROOT_FOLDER
from localstack_ext.constants import VERSION
from localstack_ext.bootstrap import licensing

CONFIG_FILE = load_file('localstack.keys.json')
if not CONFIG_FILE:
    print('WARN: No proper config file localstack.keys.json found!')
    CONFIG_FILE = '{}'
KEY_CONFIGS = json.loads(CONFIG_FILE)

BUILD_DIR = '%s/build' % ROOT_FOLDER

# whether to delete source files after encryption on build
DELETE_SOURCE_FILES = True

# AES block size
AES_BLOCK_SIZE = 16


def generate_key(version):
    if len(version.split('.')) > 3:
        version = '.'.join(version.split('.')[0:3])
    key = KEY_CONFIGS.get(version)
    if key:
        return key
    short_version = '.'.join(version.split('.')[0:2])
    return KEY_CONFIGS.get(short_version)


def get_aes_cipher(version):
    key = generate_key(version)
    return licensing.generate_aes_cipher(str(key))


def encrypt_file(source, target=None):
    cipher = get_aes_cipher(VERSION)
    if not target:
        target = '%s.enc' % source
    raw = load_file(source, mode='rb')
    raw = raw + to_bytes('\0' * (AES_BLOCK_SIZE - len(raw) % AES_BLOCK_SIZE))
    encrypter = pyaes.Encrypter(cipher)
    encrypted = encrypter.feed(raw)
    encrypted += encrypter.feed()
    save_file(target, content=encrypted)


def encrypt_files(remove=False):
    for folder in PROTECTED_FOLDERS:
        for subpath in ('*.py', '**/*.py'):
            for f in glob.glob('%s/localstack_ext/%s/%s' % (BUILD_DIR, folder, subpath)):
                if f.endswith('__init__.py'):
                    continue
                print('Encrypting %s' % f)
                encrypt_file(f)
                if remove:
                    os.remove(f)


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'encrypt':
        encrypt_files(remove=DELETE_SOURCE_FILES)
