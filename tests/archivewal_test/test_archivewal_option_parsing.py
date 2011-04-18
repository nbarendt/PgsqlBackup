from unittest import TestCase
from bbpgsql.option_parser import archivewal_parse_args
from bbpgsql.option_parser import archivewal_validate_options_and_args
from mock import patch, Mock
from testfixtures import TempDirectory


class Test_archivewal_parse_args_Uses_Common_Functions(TestCase):
    @patch('bbpgsql.option_parser.create_common_parser', spec=True)
    def test_create_common_parser_used(self, mock_func):
        mock_parser = Mock()
        mock_parser.parse_args.return_value = lambda: Mock(), []
        mock_func.return_value = mock_parser
        archivewal_parse_args(args=[])
        self.assertTrue(mock_func.called)

    @patch('bbpgsql.option_parser.create_common_parser', spec=True)
    def test_create_common_parser_passed_usage_string(self, mock_func):
        mock_parser = Mock()
        mock_parser.parse_args.return_value = lambda: Mock(), []
        mock_func.return_value = mock_parser
        archivewal_parse_args(args=[])
        kwargs = mock_func.call_args_list[0][1]
        expected_usage_suffix = '[options] <path_to_wal_file_to_archive>'
        self.assertTrue(kwargs['usage'].endswith(expected_usage_suffix))


class Test_archivewal_validate_options_Uses_Common_Functions(TestCase):
    @patch('bbpgsql.option_parser.common_validate_options_and_args', spec=True)
    def test_will_call_common_validate_options_and_args(self, mock_func):
        mock_func.return_value = False
        archivewal_validate_options_and_args()
        self.assertTrue(mock_func.called)


class Test_archivewal_requires_WAL_file(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.patchers = {}
        self.patchers['common_validate_options_and_args'] = patch(
            'bbpgsql.option_parser.common_validate_options_and_args',
            spec=True)
        self.common_validate_options_and_args_mock = self.patchers[
            'common_validate_options_and_args'].start()

    def tearDown(self):
        self.patchers['common_validate_options_and_args'].stop()
        self.tempdir.cleanup()

    def test_will_raise_exception_with_no_WAL_file(self):
        self.common_validate_options_and_args_mock.return_value = True

        def will_raise_Exception():
            archivewal_validate_options_and_args(None, [])
        self.assertRaises(Exception, will_raise_Exception)

    def test_exception_is_explicit_about_error(self):
        self.common_validate_options_and_args_mock.return_value = True
        try:
            archivewal_validate_options_and_args(None, [])
        except Exception, e:
            self.assertTrue('path to a WAL file' in str(e))

    def test_will_raise_exception_with_relative_WAL_file_path(self):
        self.common_validate_options_and_args_mock.return_value = True

        def will_raise_Exception():
            archivewal_validate_options_and_args(None, ['path_to/WAL_file'])
        self.assertRaises(Exception, will_raise_Exception)

    def test_path_to_WAL_file_must_be_absolute(self):
        self.common_validate_options_and_args_mock.return_value = True
        try:
            archivewal_validate_options_and_args(None, ['path_to/WAL_file'])
        except Exception, e:
            self.assertTrue('path to a WAL file' in str(e))

    def test_validates_if_wal_file_exists(self):
        self.common_validate_options_and_args_mock.return_value = True
        wal_file = self.tempdir.write('walfile', '')
        self.assertTrue(archivewal_validate_options_and_args(None, [wal_file]))
