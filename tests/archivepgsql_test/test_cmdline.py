from unittest import TestCase
from subprocess import check_call
from subprocess import Popen
from subprocess import PIPE
import os
from copy import deepcopy
from testfixtures import TempDirectory
from mock import patch
#from tests.cmdline_test_skeleton import Cmdline_test_skeleton
from bbpgsql.configuration import get_config_from_filename_and_set_up_logging
from bbpgsql.configuration import write_config_to_filename
from bbpgsql.configuration.repository import get_Snapshot_repository
import bbpgsql.archive_pgsql


class Test_archivepgsql_BasicCommandLineOperation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'archivepgsql'

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
        self.data_dir = self.tempdir.makedir('pgsql_data')

    def setup_config(self):
        self.config_path = os.path.join(self.tempdir.path, self.CONFIG_FILE)
        self.config_dict = {
            'General': {
                'pgsql_data_directory': self.data_dir,
            },
            'Snapshot': {
                'driver': 'memory',
            },
        }
        write_config_to_filename(self.config_dict, self.config_path)
        self.config = get_config_from_filename_and_set_up_logging(
            self.config_path
        )

    def tearDown(self):
        self.tempdir.cleanup()

    def test_can_execute_archivepgsql(self):
        check_call(self.cmd, env=self.env, stdout=PIPE)

    def test_obeys_dry_run_option(self):
        proc = Popen(self.cmd, env=self.env, stdout=PIPE)
        stdoutdata, stderrdata = proc.communicate()
        self.assertEqual("Dry Run\n", stdoutdata)


class Test_archivepgsql_backup_invocation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'archivepgsql'

    def setUp(self):
        self.setup_environment()
        self.setup_config()
        self.execution_sequence = 0

    def setup_environment(self):
        self.env = deepcopy(os.environ)
        self.env['PATH'] = ''.join([
            self.env['PATH'],
            ':',
            self.ARCHIVEPGSQL_PATH])
        self.tempdir = TempDirectory()
        self.data_dir = self.tempdir.makedir('pgsql_data')
        self.archive_dir = self.tempdir.makedir('pgsql_archive')

    def setup_config(self):
        self.config_path = os.path.join(self.tempdir.path, self.CONFIG_FILE)
        self.config_dict = {
            'General': {
                'pgsql_data_directory': self.data_dir,
            },
            'Snapshot': {
                'driver': 'memory',
            },
        }
        write_config_to_filename(self.config_dict, self.config_path)
        self.config = get_config_from_filename_and_set_up_logging(
            self.config_path
        )

    def tearDown(self):
        self.tempdir.cleanup()

    @patch('bbpgsql.archive_pgsql.commit_snapshot_to_repository')
    @patch('bbpgsql.archive_pgsql.create_archive')
    @patch('bbpgsql.archive_pgsql.pg_stop_backup')
    @patch('bbpgsql.archive_pgsql.pg_start_backup')
    def test_perform_backup(self, mock_pg_start_backup, mock_pg_stop_backup,
        mock_create_archive, mock_commit_snapshot_to_repository):
        first_WAL = '000000D0'
        second_WAL = '000000D1'
        mock_pg_start_backup.return_value = first_WAL
        mock_pg_stop_backup.return_value = second_WAL
        archiveFile = os.path.join(self.archive_dir, 'pgsql.snapshot.tar')
        tag = bbpgsql.archive_pgsql.generate_tag()
        repo = get_Snapshot_repository(self.config)
        bbpgsql.archive_pgsql.perform_backup(self.data_dir,
            archiveFile, tag, repo)
        mock_pg_start_backup.assert_called_once_with(tag)
        mock_create_archive.assert_called_once_with(self.data_dir, archiveFile)
        self.assertEqual(mock_pg_stop_backup.called, True)
        self.assertEqual(mock_pg_stop_backup.call_count, 1)
        mock_commit_snapshot_to_repository.assert_called_once_with(
            repo, archiveFile, tag, first_WAL, second_WAL)
