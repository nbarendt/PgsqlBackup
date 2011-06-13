from unittest import TestCase
from mock import patch
from bbpgsql.pg_backup_control import pg_start_backup
from bbpgsql.pg_backup_control import pg_get_version
from bbpgsql.pg_backup_control import get_pg_version_output
from bbpgsql.pg_backup_control import UnsupportedPostgresVersionError
from bbpgsql.pg_backup_control import pg_stop_backup
from bbpgsql.pg_backup_control import wal_name_cleanup


SAMPLE_8_2_7_VERSION_OUTPUT = """
psql (PostgreSQL) 8.2.7
contains support for command-line editing
"""

SAMPLE_8_3_12_VERSION_OUTPUT = """
psql (PostgreSQL) 8.3.12
contains support for command-line editing
"""

SAMPLE_8_3_7_VERSION_OUTPUT = """
psql (PostgreSQL) 8.3.7
contains support for command-line editing
"""

SAMPLE_8_4_7_VERSION_OUTPUT = """
psql (PostgreSQL) 8.4.7
contains support for command-line editing
"""

# this is entirely made up
SAMPLE_UNPARSABLE_VERSION_OUTPUT = """
psql (PSQL) 8.4a.7-rc1
contains support for command-line editing
"""

SAMPLE_UNSUPPORTED_VERSION = """
psql (PostgreSQL) 7.4.25
"""


@patch('bbpgsql.pg_backup_control.get_pg_version_output')
class Test_pg_get_version(TestCase):
    def test_parses_version_for_8_2_7_properly(self, mock_query_version):
        mock_query_version.return_value = SAMPLE_8_2_7_VERSION_OUTPUT
        self.assertEqual('8.2', pg_get_version())

    def test_parses_version_for_8_3_12_properly(self, mock_query_version):
        mock_query_version.return_value = SAMPLE_8_3_12_VERSION_OUTPUT
        self.assertEqual('8.3', pg_get_version())

    def test_parses_version_for_8_3_7_properly(self, mock_query_version):
        mock_query_version.return_value = SAMPLE_8_3_7_VERSION_OUTPUT
        self.assertEqual('8.3', pg_get_version())

    def test_parses_version_for_8_4_7_properly(self, mock_query_version):
        mock_query_version.return_value = SAMPLE_8_4_7_VERSION_OUTPUT
        self.assertEqual('8.4', pg_get_version())

    def test_raises_exception_on_unparsable_version(self, mock_query_version):
        mock_query_version.return_value = SAMPLE_UNPARSABLE_VERSION_OUTPUT

        def raises_Exception():
            pg_get_version()

        self.assertRaises(Exception, raises_Exception)

    def test_raises_UnsupportedPostgresVersionError(self, mock_query_version):
        mock_query_version.return_value = SAMPLE_UNSUPPORTED_VERSION

        def raises_Exception():
            pg_get_version()
        self.assertRaises(UnsupportedPostgresVersionError, raises_Exception)

    def test_UnsupportedPostgresVersionError_has_expected_msg(self,
        mock_query_version):
        mock_query_version.return_value = SAMPLE_UNSUPPORTED_VERSION
        try:
            pg_get_version()
        except UnsupportedPostgresVersionError, e:
            self.assertIn('Unsupported', str(e))
            self.assertIn('7.4', str(e))


@patch('bbpgsql.pg_backup_control.check_output')
class Test_get_pg_version_output(TestCase):
    def test_calls_psql_version(self, mock_check_output):
        get_pg_version_output()
        mock_check_output.assert_called_with(['psql', '--version'])


@patch('bbpgsql.pg_backup_control.pg_get_version')
@patch('bbpgsql.pg_backup_control.check_output')
class Test_pg_start_backup(TestCase):
    def setUp(self):
        self.WAL_FILENAME = '033300DF0'
        self.pgsql_return = ''.join([' ', self.WAL_FILENAME, '\n\n'])

    def tearDown(self):
        pass

    def test_function_returns_WAL_filename(self, mock_check_output, mock_vers):
        mock_vers.return_value = '8.4'
        mock_check_output.return_value = self.pgsql_return
        output = pg_start_backup('label')
        self.assertEqual(self.WAL_FILENAME, output)

    def test_check_input_arguments_correct_for_8_4(self, mock_check_output,
            mock_vers):
        mock_vers.return_value = '8.4'
        cmd_prefix = "SELECT pg_xlogfile_name(pg_start_backup('"
        label = 'label'
        cmd_suffix = "', true));"
        sql_cmd = ''.join([cmd_prefix, label, cmd_suffix])
        pg_start_backup(label)
        mock_vers.assert_called_once_with()
        mock_check_output.assert_called_with(['psql', 'postgres', '-t', '-c',
            sql_cmd])

    def test_check_input_arguments_correct_for_8_3(self, mock_check_output,
            mock_vers):
        mock_vers.return_value = '8.3'
        cmd_prefix = "SELECT pg_xlogfile_name(pg_start_backup('"
        label = 'label'
        cmd_suffix = "'));"
        sql_cmd = ''.join([cmd_prefix, label, cmd_suffix])
        pg_start_backup(label)
        mock_vers.assert_called_once_with()
        mock_check_output.assert_called_with(['psql', 'postgres', '-t', '-c',
            sql_cmd])

    def test_wal_name_cleanup(self, mock_check_output, mock_vers):
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
