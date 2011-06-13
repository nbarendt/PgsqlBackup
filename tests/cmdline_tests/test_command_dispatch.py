from unittest import TestCase
from mock import patch
from bbpgsql.bbpgsql_main import bbpgsql_main


@patch('bbpgsql.bbpgsql_main.bbpgsql_error')
@patch('bbpgsql.bbpgsql_main.archivewal_main')
@patch('bbpgsql.bbpgsql_main.archivepgsql_main')
class Test_command_dispatch(TestCase):
    archivepgsql_exe = 'archivepgsql'
    archivewal_exe = 'archivewal'
    bbpgsql_exe = 'bbpgsql'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dispatch_calls_archivepgsql_main(self,
        mock_archivepgsql_main, mock_archivewal_main, mock_bbpgsql_error):
        fake_argv = [self.archivepgsql_exe]
        bbpgsql_main(fake_argv)
        mock_archivepgsql_main.assert_called_once_with()
        self.assertFalse(mock_archivewal_main.called)
        self.assertFalse(mock_bbpgsql_error.called)

    def test_dispatch_calls_only_archivewal_main(self,
        mock_archivepgsql_main, mock_archivewal_main, mock_bbpgsql_error):
        fake_argv = [self.archivewal_exe]
        bbpgsql_main(fake_argv)
        mock_archivewal_main.assert_called_once_with()
        self.assertFalse(mock_archivepgsql_main.called)
        self.assertFalse(mock_bbpgsql_error.called)

    def test_dispatch_calls_only_bbpgsql_error(self,
        mock_archivepgsql_main, mock_archivewal_main, mock_bbpgsql_error):
        fake_argv = [self.bbpgsql_exe]
        bbpgsql_main(fake_argv)
        mock_bbpgsql_error.assert_called_once_with()
        self.assertFalse(mock_archivepgsql_main.called)
        self.assertFalse(mock_archivewal_main.called)


@patch('bbpgsql.bbpgsql_main.stdout.write')
@patch('bbpgsql.bbpgsql_main.exit')
class Test_incorrect_invocation(TestCase):
    mainMsg = '''You have invoked this script as bbpgsql.
This script is supposed to be invoked through the commands archivepgsql
and archivewal.  Please check with your adminstrator to make sure these
commands were installed correctly.
'''
    unknownMsg = 'Unknown command: unknown\n'

    def test_invokation_using_main_script_fails(self,
        mock_exit, mock_stdout_write):
        bbpgsql_main(['bbpgsql'])
        mock_stdout_write.assert_called_once_with(self.mainMsg)
        mock_exit.assert_called_once_with(1)

    def test_invocation_using_unknown_fails(self,
        mock_exit, mock_stdout_write):
        bbpgsql_main(['unknown'])
        mock_stdout_write.assert_called_once_with(self.unknownMsg)
        mock_exit.assert_called_once_with(1)
