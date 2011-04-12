from unittest import TestCase
from subprocess import Popen, PIPE, STDOUT
import os
from uuid import uuid4
from copy import deepcopy
from testfixtures import TempDirectory
from ConfigParser import SafeConfigParser
from boto import connect_s3


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
        configFile = SafeConfigParser()
        configFile.read('aws_test.ini')
        self.aws_access_key = configFile.get('aws', 'aws_access_key')
        self.aws_secret_key = configFile.get('aws', 'aws_secret_key')
        self.s3_connection = connect_s3(self.aws_access_key,
            self.aws_secret_key)
        self.bucket_name = '.'.join(['test', uuid4().hex])
        self.prefix = 'wal/'

    def setup_config(self):
        self.config_path = self.tempdir.getpath(self.CONFIG_FILE)
        f = open(self.config_path, 'wb')
        f.write("""
[WAL storage]
driver=s3
bucket={0}
prefix={1}
[Credentials]
aws_access_key_id={2}
aws_secret_key_id={3}
""".format(self.bucket_name, self.prefix,
            self.aws_access_key, self.aws_secret_key))
        f.close()
        #print '----'
        #print open(self.config_path, 'rb').read()
        #print '----'

    def tearDown(self):
        self.teardown_bucket()
        self.tempdir.cleanup()

    def get_bucket(self):
        return self.s3_connection.create_bucket(self.bucket_name)

    def teardown_bucket(self):
        bucket = self.get_bucket()
        for key in bucket:
            key.delete()
        bucket.delete()

    def test_will_archive_WAL_file_to_S3(self):
        WAL_CONTENTS = 'some data'
        WAL_FILENAME = 'walfile'
        wal_file_path = self.tempdir.write(WAL_FILENAME, WAL_CONTENTS)
        self.cmd.append(wal_file_path)
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print proc.stdout.read()
        self.assertEqual(0, proc.returncode)
        self.validate_wal_file(WAL_FILENAME, WAL_CONTENTS)

    def validate_wal_file(self, wal_filename, wal_contents):
        keys = [k.name for k in self.get_bucket()]
        self.assertEqual(1, len(keys))
        wal_keyname = keys[0]
        print "wal_keyname", wal_keyname
        expected_keyname_prefix = ''.join([self.prefix, wal_filename])
        self.assertTrue(wal_keyname.startswith(expected_keyname_prefix))
        key = self.get_bucket().get_key(wal_keyname)
        self.assertEqual(wal_contents, key.get_contents_as_string())
