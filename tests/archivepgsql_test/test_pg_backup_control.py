from unittest import TestCase
from mock import patch
from bbpgsql.pg_backup_control import pg_start_backup
from bbpgsql.pg_backup_control import pg_stop_backup
from bbpgsql.pg_backup_control import wal_name_cleanup

@patch('bbpgsql.pg_backup_control.check_output')
class Test_pg_start_backup(TestCase):
    def setUp(self):
        self.WAL_FILENAME = '033300DF0'
        self.pgsql_return = ''.join([' ', self.WAL_FILENAME, '\n\n'])

    def tearDown(self):
        pass

    def test_function_returns_WAL_filename(self, mock_check_output):
        mock_check_output.return_value = self.pgsql_return
        output = pg_start_backup('label')
        self.assertEqual(self.WAL_FILENAME, output)

    def test_check_input_arguments_correct(self, mock_check_output):
        cmd_prefix = "SELECT pg_xlogfile_name(pg_start_backup('"
        label = 'label'
        cmd_suffix = "', true));"
        sql_cmd = ''.join([cmd_prefix, label, cmd_suffix])
        pg_start_backup(label)
        mock_check_output.assert_called_with(['psql', 'postgres', '-t', '-c', sql_cmd])

    def test_wal_name_cleanup(self, mock_check_output):
        output = wal_name_cleanup(self.pgsql_return)
        self.assertEqual(self.WAL_FILENAME, output)


@patch('bbpgsql.pg_backup_control.check_output')
class Test_pg_stop_backup(TestCase):
    def setUp(self):
        self.WAL_FILENAME = '033300DF0'
        self.pgsql_return = ''.join([' ', self.WAL_FILENAME, '\n\n'])

    def tearDown(self):
        pass

    def test_check_returns_WAL_filename(self, mock_check_output):
        mock_check_output.return_value = self.pgsql_return
        output = pg_stop_backup()
        self.assertEqual(self.WAL_FILENAME, output)

    def test_check_input_arguments_correct(self, mock_check_output):
        sql_cmd = "SELECT pg_xlogfile_name(pg_stop_backup())"
        pg_stop_backup()
        mock_check_output.assert_called_with(['psql',
            'postgres', '-t', '-c', sql_cmd])

    def test_wal_name_cleanup(self, mock_check_output):
        output = wal_name_cleanup(self.pgsql_return)
        self.assertEqual(self.WAL_FILENAME, output)
