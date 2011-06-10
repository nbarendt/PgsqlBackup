from unittest import TestCase
import os
from uuid import uuid4
from copy import deepcopy
from testfixtures import TempDirectory
from tests.integration.s3_helpers import setup_s3_and_bucket
from bbpgsql.configuration import write_config_to_filename

class S3_Integration_Test_Skeleton(TestCase):
    __test__ = False # to prevent nose from running this skeleton
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'fill this in with your command'
    ONE_MEBIBYTE = 1024. * 1024.
    ONE_MEGABYTE = 1000. * 1000.


    def setUp(self):
        raise Exception('This is a skeleton for test - you need to provide'
                        ' your own setUp() and tearDown()')

    def setUp_s3_common(self):
        self.setup_environment()
        self.setup_config()
        self.cmd = [self.exe_script, '--config', self.config_path]

    def setup_environment(self):
        self.env = deepcopy(os.environ)
        self.env['PATH'] = ''.join([
            self.env['PATH'],
            ':',
            self.ARCHIVEPGSQL_PATH])
        self.tempdir = TempDirectory()

    def setup_s3(self):
        self.bucket_name = '.'.join(['test', uuid4().hex])
        self.prefix = 'wals/'
        self.temps3 = setup_s3_and_bucket(self.bucket_name)

    def setup_config(self):
        self.setup_s3()
        self.config_path = self.tempdir.getpath(self.CONFIG_FILE)
        config_dict = {
            'General': {
                'pgsql_data_directory': self.tempdir.path,
                'bucket': self.bucket_name,
            },
            'Credentials': {
                'aws_access_key_id': self.temps3.access_key,
                'aws_secret_key_id': self.temps3.secret_key,
            },
        }
        write_config_to_filename(config_dict, self.config_path)

    def tearDown_s3_common(self):
        self.temps3.cleanup()
        self.tempdir.cleanup()
