from unittest import TestCase
import os
from mock import patch
from bbpgsql.bbpgsql_main import bbpgsql_main
from testfixtures import TempDirectory
from bbpgsql.configuration import write_config_to_filename


@patch('bbpgsql.bbpgsql_main.bbpgsql_error')
@patch('bbpgsql.bbpgsql_main.archivewal_main')
@patch('bbpgsql.bbpgsql_main.archivepgsql_main')
@patch('bbpgsql.bbpgsql_main.restorewal_main')
class Test_command_dispatch(TestCase):
    archivepgsql_exe = 'archivepgsql'
    archivewal_exe = 'archivewal'
    restorewal_exe = 'restorewal'
    restorepgsql_exe = 'restorepgsql'
    bbpgsql_exe = 'bbpgsql'

    def setUp(self):
        self.tempdir = TempDirectory()
        self.config_dict = {
        }
        self.config_path = os.path.join(self.tempdir.path, 'config.ini')
        write_config_to_filename(self.config_dict, self.config_path)

    def tearDown(self):
        self.tempdir.cleanup()

    def get_argv_for_cmd(self, cmd):
        return [cmd, '-c', self.config_path]

    def test_dispatch_calls_only_archivepgsql_main(self,
        mock_restorewal_main,
        mock_archivepgsql_main,
        mock_archivewal_main,
        mock_bbpgsql_error
        ):
        bbpgsql_main(self.get_argv_for_cmd(self.archivepgsql_exe))
        mock_archivepgsql_main.assert_called_once_with()
        self.assertFalse(mock_archivewal_main.called)
        self.assertFalse(mock_restorewal_main.called)
        self.assertFalse(mock_bbpgsql_error.called)

    def test_dispatch_calls_only_archivewal_main(self,
        mock_restorewal_main,
        mock_archivepgsql_main,
        mock_archivewal_main,
        mock_bbpgsql_error
        ):
        bbpgsql_main(self.get_argv_for_cmd(self.archivewal_exe))
        mock_archivewal_main.assert_called_once_with()
        self.assertFalse(mock_archivepgsql_main.called)
        self.assertFalse(mock_restorewal_main.called)
        self.assertFalse(mock_bbpgsql_error.called)

    def test_dispatch_calls_only_restorewal_main(self,
        mock_restorewal_main,
        mock_archivepgsql_main,
        mock_archivewal_main,
        mock_bbpgsql_error
        ):
        bbpgsql_main(self.get_argv_for_cmd(self.restorewal_exe))
        mock_restorewal_main.assert_called_once_with()
        self.assertFalse(mock_archivepgsql_main.called)
        self.assertFalse(mock_archivewal_main.called)
        self.assertFalse(mock_bbpgsql_error.called)


    def test_dispatch_calls_only_bbpgsql_error(self,
        mock_restorewal_main,
        mock_archivepgsql_main,
        mock_archivewal_main,
        mock_bbpgsql_error
        ):
        bbpgsql_main(self.get_argv_for_cmd(self.bbpgsql_exe))
        mock_bbpgsql_error.assert_called_once_with()
        self.assertFalse(mock_archivepgsql_main.called)
        self.assertFalse(mock_archivewal_main.called)
        self.assertFalse(mock_restorewal_main.called)


class Test_incorrect_invocation(TestCase):
    mainMsg = '''You have invoked this script as bbpgsql.
This script is supposed to be invoked through the commands archivepgsql
and archivewal.  Please check with your adminstrator to make sure these
commands were installed correctly.
'''
    unknownMsg = 'Unknown command: unknown\n'

    def setUp(self):
        self.tempdir = TempDirectory()
        self.config_dict = {
        }
        self.config_path = os.path.join(self.tempdir.path, 'config.ini')
        write_config_to_filename(self.config_dict, self.config_path)

    def tearDown(self):
        self.tempdir.cleanup()

    @patch('bbpgsql.bbpgsql_main.exit')
    def test_invocation_using_main_script_fails(self,
        mock_exit):
        bbpgsql_main(['bbpgsql', '-c', self.config_path])
        mock_exit.assert_called_with(1)

    @patch('bbpgsql.bbpgsql_main.stdout.write')
    @patch('bbpgsql.bbpgsql_main.exit')
    def test_invocation_using_unknown_fails(self,
        mock_exit, mock_stdout_write):
        bbpgsql_main(['unknown'])
        mock_stdout_write.assert_called_once_with(self.unknownMsg)
        mock_exit.assert_called_once_with(1)
