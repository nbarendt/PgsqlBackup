from unittest import TestCase
from subprocess import Popen, PIPE, STDOUT
import os
from copy import deepcopy
from testfixtures import TempDirectory
from bbpgsql.configuration import write_config_to_filename


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
        self.storage_path = self.tempdir.makedir('repo')
        self.config_path = self.tempdir.getpath(self.CONFIG_FILE)
        self.log_file = self.tempdir.getpath('bbpgsql.log')
        self.config_dict = {
            'WAL':  {
                'driver': 'filesystem',
                'path': self.storage_path,
            },
            'General': {
                'pgsql_data_directory': self.tempdir.path,
            },
            'Logging': {
                'logfile': self.log_file
            },
        }
        write_config_to_filename(self.config_dict, self.config_path)
        #print '----'
        #print open(self.config_path, 'rb').read()
        #print '----'
        self.pg_xlog_path = 'pg_xlog'
        self.tempdir.makedir(self.pg_xlog_path)
        self.wal_basename = '00001'
        self.wal_filename = os.path.join(self.pg_xlog_path, self.wal_basename)
        self.tempdir.write(self.wal_filename, '')
        print 'TEMPDIR', self.tempdir.listdir(recursive=True)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_archivewal_returns_error_with_if_less_than_one_argument(self):
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print(proc.stdout.read())
        self.assertNotEqual(0, proc.returncode)

    def test_archivewal_logs_error_with_if_less_than_one_argument(self):
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        log_output = open(self.log_file, 'rb').read()
        print 'log_output:'
        print log_output
        assert 'ERROR' in log_output

    def test_archivewal_success_with_file(self):
        self.cmd.append(self.wal_filename)
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print proc.stdout.read()
        self.assertEqual(0, proc.returncode)

    def test_archivewal_actually_archives_file(self):
        self.cmd.append(self.wal_filename)
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        print proc.stdout.read()
        self.assertEqual(0, proc.returncode)
        archives = os.listdir(self.storage_path)
        print archives
        self.assertTrue(archives[0].startswith(''.join([
            self.wal_basename, '_'])))
