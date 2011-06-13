from subprocess import Popen, PIPE, STDOUT
from tests.integration.s3_integration_skeleton import (
    S3_Integration_Test_Skeleton
)
from gzip import GzipFile
from StringIO import StringIO

class Test_archivewal_commits_to_S3(S3_Integration_Test_Skeleton):
    __test__ = True # to make nose run this class
    exe_script = 'archivewal'
    prefix = 'wals/'

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
