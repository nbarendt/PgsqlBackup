from subprocess import Popen, PIPE, STDOUT, check_call
from tests.integration.s3_integration_skeleton import (
    S3_Integration_Test_Skeleton
)
import filecmp
import os.path


class Test_restorewal_retrieves_from_S3(S3_Integration_Test_Skeleton):
    __test__ = True  # to make nose run this class
    exe_script = 'restorewal'
    prefix = 'wals/'

    def setup_environment_and_paths_customize(self):
        self.waldestdirpath = self.tempdir.makedir('waldest')

    def setup_customize(self):
        WAL_CONTENTS = 'some data'
        WAL_FILENAME = 'walfile'
        self.waldestfilepath = os.path.join(self.waldestdirpath, WAL_FILENAME)
        self.srcfilepath = self.tempdir.write(WAL_FILENAME, WAL_CONTENTS)
        self.destfilepath = os.path.join(self.waldestdirpath, WAL_FILENAME)
        self.cmd.append(WAL_FILENAME)
        self.cmd.append(self.waldestfilepath)
        self.archivecmd = [
            'archivewal',
            '--config',
            self.config_path,
            WAL_FILENAME
            ]
        check_call(self.archivecmd, env=self.env, stdout=PIPE, stderr=STDOUT)

    def test_will_restore_WAL_file_from_S3(self):
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print(proc.stdout.read())
        self.assertEqual(0, proc.returncode)
        self.assertTrue(filecmp.cmp(
            self.srcfilepath,
            self.destfilepath,
            shallow=False
            ))
