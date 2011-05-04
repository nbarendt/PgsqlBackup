from unittest import TestCase
from subprocess import Popen, PIPE, STDOUT
import os
from uuid import uuid4
from copy import deepcopy
from testfixtures import TempDirectory
from tests.integration.s3_helpers import setup_s3_and_bucket
from bbpgsql.configuration import write_config_to_filename
from gzip import GzipFile
from StringIO import StringIO

class Test_archivewal_commits_to_S3(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'archivewal'

    def setUp(self):
        self.setup_environment()
        self.setup_s3()
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
        self.config_path = self.tempdir.getpath(self.CONFIG_FILE)
        config_dict = {
            'General': {
                'pgsql_data_directory': self.tempdir.path,
                'bucket': self.bucket_name,
            },
            'WAL': {
            },
            'Credentials': {
                'aws_access_key_id': self.temps3.access_key,
                'aws_secret_key_id': self.temps3.secret_key,
            },
        }
        write_config_to_filename(config_dict, self.config_path)

    def tearDown(self):
        self.temps3.cleanup()
        self.tempdir.cleanup()

    def test_will_archive_WAL_file_to_S3(self):
        WAL_CONTENTS = 'some data'
        WAL_FILENAME = 'walfile'
        self.tempdir.write(WAL_FILENAME, WAL_CONTENTS)
        self.cmd.append(WAL_FILENAME)
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print proc.stdout.read()
        self.assertEqual(0, proc.returncode)
        self.validate_wal_file(WAL_FILENAME, WAL_CONTENTS)

    def validate_wal_file(self, wal_filename, wal_contents):
        keys = [k.name for k in self.temps3.bucket]
        self.assertEqual(1, len(keys))
        wal_keyname = keys[0]
        print "wal_keyname", wal_keyname
        expected_keyname_prefix = ''.join([self.prefix, wal_filename])
        self.assertTrue(wal_keyname.startswith(expected_keyname_prefix))
        key = self.temps3.bucket.get_key(wal_keyname)
        compressed_wal_data = key.get_contents_as_string()
        compressed_wal_fp = StringIO(compressed_wal_data)
        uncompressed_data = GzipFile(fileobj=compressed_wal_fp).read()
        self.assertEqual(wal_contents, uncompressed_data)
