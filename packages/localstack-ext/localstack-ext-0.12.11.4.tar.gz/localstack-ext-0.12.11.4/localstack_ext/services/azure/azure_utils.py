# flake8:noqa

import re
import asyncio
import logging
from six.moves.urllib import parse as urlparse
from localstack.utils.common import to_str
from localstack_ext import config as config_ext

LOG = logging.getLogger(__name__)

REGEX_FLAGS = re.DOTALL | re.IGNORECASE

REGIONS = ['Central US', 'West US', 'East US', 'East US 2', 'West US 2', 'South Africa North',
    'North Central US', 'South Central US', 'West Central US', 'East US 2 EUAP', 'Central US EUAP',
    'UK West', 'North Europe', 'West Europe', 'Brazil South', 'Australia East', 'Australia Southeast',
    'Southeast Asia', 'East Asia', 'Japan West', 'Japan East', 'Central India', 'West India', 'South India',
    'Canada Central', 'Canada East', 'Korea Central', 'Australia Central', 'Australia Central 2']


def get_azure_endpoint():
    return 'https://%s' % get_azure_host()


def get_azure_host():
    return '%s:%s' % (config_ext.LOCAL_HOSTNAME, config_ext.PORT_AZURE)


def get_scm_url(app_name):
    return 'https://%s.scm.%s' % (app_name, get_azure_host())


def get_ftp_host():
    return 'ftp.%s' % get_azure_host()


def path_matches(path, pattern):
    path_path, _, path_query = path.partition('?')
    pattern_path, _, pattern_query = pattern.partition('?')

    path_query_dict = parse_qs(path_query)
    pattern_query_dict = parse_qs(pattern_query)
    for k, v in dict(pattern_query_dict).items():
        if re.match(r'^\{.*\}$', v):
            pattern_query_dict.pop(k)
            path_query_dict.pop(k, None)
    all_contained = set(pattern_query_dict.keys()).issubset(set(path_query_dict.keys()))
    if not all_contained:
        return False

    # certain path parameters may contain arbitrary characters (including '/')
    for placeholder in ['{blob}']:
        pattern_path = pattern_path.replace(placeholder, '.+')

    pattern_path = re.sub(r'\{[^\}]+\}', r'[^/]+', pattern_path)
    pattern_path = '^%s$' % pattern_path
    if not re.match(pattern_path, path_path, flags=REGEX_FLAGS):
        return False

    return True


def parse_qs(query):
    result = urlparse.parse_qs(to_str(query), keep_blank_values=True)
    result = dict([(k, v[0]) for k, v in result.items()])
    return result


def get_matching_paths(path, patterns):
    matches = set()
    for pattern in patterns:
        if path_matches(path, pattern):
            matches.add(pattern)
    if not matches:
        return
    return list(matches)


def log(msg, *args, **kwargs):
    LOG.info(msg, *args, **kwargs)
    print(msg, *args, **kwargs)


class SASLHandshake:

    INSTANCES = {}
    STEPS = [
        ('OUT', b'AMQP\x03\x01\x00\x00'),
        ('IN', b'AMQP\x03\x01\x00\x00\x00\x00\x00?\x02\x01\x00\x00\x00S@\xc02\x01\xe0/\x04\xb3\x00\x00\x00\x07MSSBCBS\x00\x00\x00\x05PLAIN\x00\x00\x00\tANONYMOUS\x00\x00\x00\x08EXTERNAL'),
        ('OUT', b'\x00\x00\x00\x17\x02\x01\x00\x00\x00SA\xc0\n\x01\xa3\x07MSSBCBS'),
        ('IN', b'\x00\x00\x00\x1a\x02\x01\x00\x00\x00SD\xc0\r\x02P\x00\xa0\x08Welcome!'),
        ('OUT', b'AMQP\x00\x01\x00\x00'),
        ('IN', b'AMQP\x00\x01\x00\x00'),
        ('OUT', b'\x00\x00\x01D\x02\x00\x00\x00\x00S\x10\xd0\x00\x00\x014\x00\x00\x00\n\xa1-SBSender-511cfc4d-d29b-4b8e-9a39-afe0af30e3da\xa1\x1ftest.localhost.localstack.cloudp\x00\x01\x00\x00`\xff\xff@@@@@\xc1\xd1\n\xa3\x07product\xa1\x17azsdk-python-servicebus\xa3\x07version\xa1\x057.0.1\xa3\tframework\xa1\x0cPython/3.8.2\xa3\x08platform\xa1\x1fmacOS-10.15.7-x86_64-i386-64bit\xa3\nuser-agent\xa1Lazsdk-python-servicebus/7.0.1 Python/3.8.2 (macOS-10.15.7-x86_64-i386-64bit)'),
        ('IN', b'\x00\x00\x00G\x02\x00\x00\x00\x00S\x10\xc0:\n\xa1$154aa1f6195741abab1add27629287bf_G22@p\x00\x01\x00\x00`\x13\x87p\x00\x03\xa9\x80@@@@@'),
        ('OUT', b'\x00\x00\x00\x1f\x02\x00\x00\x00\x00S\x11\xc0\x12\x05@Cp\x00\x01\x00\x00p\x00\x01\x00\x00p\xff\xff\xff\xff'),
        ('IN', b'\x00\x00\x00"\x02\x00\x00\x00\x00S\x11\xc0\x15\x08`\x00\x00R\x01p\x00\x00\x13\x88p\x00\x01\x00\x00R\xff@@@'),
        ('OUT', b'\x00\x00\x00=\x02\x00\x00\x00\x00S\x12\xc00\x0b\xa1\x0b$cbs-senderCBP\x00P\x00\x00S(\xc0\x07\x01\xa1\x04$cbs\x00S)\xc0\x07\x01\xa1\x04$cbs@@CD\x00\x00\x00@\x02\x00\x00\x00\x00S\x12\xc03\x0b\xa1\r$cbs-receiverR\x01AP\x00P\x00\x00S(\xc0\x07\x01\xa1\x04$cbs\x00S)\xc0\x07\x01\xa1\x04$cbs@@@D'),
        ('IN', b'\x00\x00\x00X\x02\x00\x00\x00\x00S\x12\xc0K\x0e\xa1\x0b$cbs-senderCAP\x00P\x00\x00S(\xc0\x11\x0b\xa1\x04$cbs@@@@@@@@@@\x00S)\xc0\r\x07\xa1\x04$cbs@@@@@@@@@\x80\xff\xff\xff\xff\xff\xff\xff\xff@@@\x00\x00\x00#\x02\x00\x00\x00\x00S\x13\xc0\x16\x0bCp\x00\x00\x13\x88R\x01p\x00\x01\x00\x00CCRdC@B@'),
        ('IN', b'\x00\x00\x00[\x02\x00\x00\x00\x00S\x12\xc0N\x0e\xa1\r$cbs-receiverR\x01BP\x00P\x00\x00S(\xc0\x11\x0b\xa1\x04$cbs@@@@@@@@@@\x00S)\xc0\r\x07\xa1\x04$cbs@@@@@@@@C\x80\xff\xff\xff\xff\xff\xff\xff\xff@@@'),
        ('IN', b'\x00\x00\x00[\x02\x00\x00\x00\x00S\x12\xc0N\x0e\xa1\r$cbs-receiverR\x01BP\x00P\x00\x00S(\xc0\x11\x0b\xa1\x04$cbs@@@@@@@@@@\x00S)\xc0\r\x07\xa1\x04$cbs@@@@@@@@C\x80\xff\xff\xff\xff\xff\xff\xff\xff@@@'),
        ('OUT', b"\x00\x00\x01L\x02\x00\x00\x00\x00S\x14\xc0\x0c\x06CC\xa0\x04\x01\x00\x00\x00CBB\x00Ss\xc0\x02\x01D\x00St\xc1t\x06\xa1\x04name\xa1.sb://test.localhost.localstack.cloud/testqueue\xa1\toperation\xa1\tput-token\xa1\x04type\xa1\x1fservicebus.windows.net:sastoken\x00Sw\xa1\xaeSharedAccessSignature sr=sb%3A%2F%2Ftest.localhost.localstack.cloud%2Ftestqueue&sig=foobarfoobar4EE2VEghLGd4NNNTTI3VjXNcvzFWVPM%3d&se=1613945714&skn=RootManageSharedAccessKey\x00\x00\x00$\x02\x00\x00\x00\x00S\x13\xc0\x17\x07R\x01p\x00\x01\x00\x00R\x01p\x00\x00\xff\xffR\x01Cp\x00\x00'\x10")
    ]

    def __init__(self):
        self.step = 0

    def steps(self, outgoing):
        async def iterator():
            while self.step < len(self.STEPS):
                next_step = self.STEPS[self.step]
                is_out_step = next_step[0] == 'OUT'
                if bool(outgoing) != bool(is_out_step):
                    await asyncio.sleep(0.2)
                    continue
                yield next_step[1]
                self.step += 1
        return iterator()

    @classmethod
    def get_steps(cls, context, outgoing):
        instance = cls.get(context)
        return instance.steps(outgoing)

    @classmethod
    def get(cls, context):
        idx = id(context)
        existing = instance = cls.INSTANCES.pop(idx, None)
        if not instance:
            instance = cls.INSTANCES[idx] = SASLHandshake()
        return instance, bool(existing)
