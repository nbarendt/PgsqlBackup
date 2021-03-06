from unittest import TestCase
from bbpgsql.option_parser import archivewal_parse_args
from bbpgsql.option_parser import archivewal_validate_options_and_args
from bbpgsql.configuration import write_config_to_filename
from mock import patch, Mock
from testfixtures import TempDirectory
from optparse import OptionParser
import os


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


class Test_archivewal_parse_arges_returns_parser_options_args(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.config_dict = {
            'General': {
                'pgsql_data_directory': self.tempdir.path,
            },
        }
        self.config_file = os.path.join(self.tempdir.path, 'config_file')
        write_config_to_filename(self.config_dict, self.config_file)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_archivewal_parse_args_returns_three_items(self):
        item1, item2, item3 = archivewal_parse_args(args=['walfilename'])
        self.assertNotEqual(type(item1), type(None))
        self.assertNotEqual(type(item2), type(None))
        self.assertNotEqual(type(item3), type(None))

    def test_archivewal_parse_args_returns_parser(self):
        parser, item2, item3 = archivewal_parse_args(args=['walfilename'])
        self.assertTrue(isinstance(parser, OptionParser))

    def test_archivewal_parse_args_returns_options(self):
        item1, options, item3 = archivewal_parse_args(args=['walfilename'])
        self.assertTrue(isinstance(options, object))

    def test_archivewal_parse_args_returns_args(self):
        item1, item2, args = archivewal_parse_args(args=['walfilename'])
        self.assertEqual(type(args), type([]))


class Test_archivewal_validate_options_Uses_Common_Functions(TestCase):
    @patch('bbpgsql.option_parser.common_validate_options_and_args', spec=True)
    def test_will_call_common_validate_options_and_args(self, mock_func):
        mock_func.return_value = False
        retval = archivewal_validate_options_and_args()
        self.assertTrue(mock_func.called)
        self.assertFalse(retval)


class Test_archivewal_requires_WAL_file(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.config_dict = {
            'General': {
                'pgsql_data_directory': self.tempdir.path,
            },
        }
        self.config_file = os.path.join(self.tempdir.path, 'config_file')
        write_config_to_filename(self.config_dict, self.config_file)
        parser, self.options, self.args = archivewal_parse_args(['-c',
            self.config_file])

    def tearDown(self):
        self.tempdir.cleanup()

    def test_will_raise_exception_with_no_WAL_file(self):

        def will_raise_Exception():
            archivewal_validate_options_and_args(self.options, [])
        self.assertRaises(Exception, will_raise_Exception)

    def test_exception_is_explicit_about_error(self):
        try:
            archivewal_validate_options_and_args(self.options, [])
        except Exception, e:
            print 'Exception', e
            self.assertTrue('path to a WAL file' in str(e))
        else:
            self.assertTrue(False, 'should never get here')

    def test_path_to_WAL_file_must_be_relative(self):
        abs_wal_path = self.tempdir.write('WAL_file', '')

        def raises_exception():
            archivewal_validate_options_and_args(self.options, [abs_wal_path])
        self.assertRaises(Exception, raises_exception)

    def test_validates_if_wal_file_exists(self):
        wal_filename = 'WAL_file'
        self.tempdir.write(wal_filename, '')
        self.assertTrue(archivewal_validate_options_and_args(self.options,
            [wal_filename]))
