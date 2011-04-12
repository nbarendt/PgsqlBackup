from unittest import TestCase
from subprocess import Popen, PIPE, STDOUT
import os
from copy import deepcopy
from testfixtures import TempDirectory


class Test_archivepgsql_BasicCommandLineOperation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'archivewal'

    def setUp(self):
        self.setup_environment()
        self.setup_config()
        self.cmd = [self.exe_script, '--dry-run', '--config', self.config_path]

    def setup_environment(self):
        self.env = deepcopy(os.environ)
        self.env['PATH'] = ''.join([
            self.env['PATH'],
            ':',
            self.ARCHIVEPGSQL_PATH])
        self.tempdir = TempDirectory()

    def setup_config(self):
        self.config_path = self.tempdir.getpath(self.CONFIG_FILE)
        self.storage_path = self.tempdir.makedir('repo')
        f = open(self.config_path, 'wb')
        f.write("""
[WAL storage]
driver=filesystem
path={0}
""".format(self.storage_path))
        f.close()
        #print '----'
        #print open(self.config_path, 'rb').read()
        #print '----'

    def tearDown(self):
        self.tempdir.cleanup()

    def test_archivewal_returns_error_with_if_less_than_one_argument(self):
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print(proc.stdout.read())
        self.assertNotEqual(0, proc.returncode)

    def test_archivewal_success_with_file(self):
        wal_filename = self.tempdir.write('walfile', '')
        self.cmd.append(wal_filename)
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print proc.stdout.read()
        self.assertEqual(0, proc.returncode)

    def test_archivewal_actually_archives_file(self):
        wal_filename = self.tempdir.write('walfile', '')
        self.cmd.append(wal_filename)
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print proc.stdout.read()
        self.assertEqual(0, proc.returncode)
        archives = os.listdir(self.storage_path)
        print archives
        self.assertTrue(archives[0].startswith('walfile_'))
