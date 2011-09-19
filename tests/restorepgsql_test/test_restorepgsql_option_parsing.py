from unittest import TestCase
from bbpgsql.option_parser import restorepgsql_parse_args
from bbpgsql.option_parser import restorepgsql_validate_options_and_args
from bbpgsql.configuration import write_config_to_filename
from mock import patch, Mock
from testfixtures import TempDirectory
from optparse import OptionParser
import os


class Test_restorepgsql_parse_args_Uses_Common_Functions(TestCase):
    @patch('bbpgsql.option_parser.create_common_parser', spec=True)
    def test_create_common_parser_used(self, mock_func):
        mock_parser = Mock()
        mock_parser.parse_args.return_value = lambda: Mock(), []
        mock_func.return_value = mock_parser
        restorepgsql_parse_args(args=[])
        self.assertTrue(mock_func.called)

    @patch('bbpgsql.option_parser.create_common_parser', spec=True)
    def test_create_common_parser_passed_usage_string(self, mock_func):
        mock_parser = Mock()
        mock_parser.parse_args.return_value = lambda: Mock(), []
        mock_func.return_value = mock_parser
        restorepgsql_parse_args(args=[])
        kwargs = mock_func.call_args_list[0][1]
        expected_usage_suffix = ' '.join([
            '[options]',
            ])
        self.assertTrue(kwargs['usage'].endswith(expected_usage_suffix))


class Test_restorepgsql_parse_args_returns_parser_options_args(TestCase):
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

    def test_restorepgsql_parse_args_returns_three_items(self):
        item1, item2, item3 = restorepgsql_parse_args()
        self.assertNotEqual(type(item1), type(None))
        self.assertNotEqual(type(item2), type(None))
        self.assertNotEqual(type(item3), type(None))

    def test_restorepgsql_parse_args_returns_parser(self):
        parser, item2, item3 = restorepgsql_parse_args(args=None)
        self.assertTrue(isinstance(parser, OptionParser))

    def test_restorepgsql_parse_args_returns_options(self):
        item1, options, item3 = restorepgsql_parse_args(args=None)
        self.assertTrue(isinstance(options, object))

    def test_restorepgsql_parse_args_returns_args(self):
        item1, item2, args = restorepgsql_parse_args(args=None)
        self.assertEqual(type(args), type([]))


class Test_restorepgsql_validate_options_Uses_Common_Functions(TestCase):
    @patch('bbpgsql.option_parser.common_validate_options_and_args', spec=True)
    def test_will_call_common_validate_options_and_args(self, mock_func):
        mock_func.return_value = False
        retval = restorepgsql_validate_options_and_args()
        self.assertTrue(mock_func.called)
        self.assertFalse(retval)


class Test_restorepgsql_requires_pgsql_file_and_destination(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.config_dict = {
            'General': {
                'pgsql_data_directory': self.tempdir.path,
            },
        }
        self.config_file = os.path.join(self.tempdir.path, 'config_file')
        write_config_to_filename(self.config_dict, self.config_file)
        parser, self.options, self.args = restorepgsql_parse_args(['-c',
            self.config_file])

    def tearDown(self):
        self.tempdir.cleanup()

    def test_will_raise_exception_if_not_exactly_zero_args(self):
        self.assertRaises(
            Exception,
            restorepgsql_validate_options_and_args,
            self.options,
            ['one']
            )
        self.assertRaises(
            Exception,
            restorepgsql_validate_options_and_args,
            self.options,
            ['one', 'two']
            )
        self.assertRaises(
            Exception,
            restorepgsql_validate_options_and_args,
            self.options,
            ['one', 'two', 'three']
            )

    def test_is_explicit_about_error(self):
        try:
            restorepgsql_validate_options_and_args(
                self.options,
                ['one']
                )
        except Exception, e:
            print 'Exception', e
            self.assertTrue('called with no arguments' in str(e))
        else:
            self.assertTrue(False, 'should never get here')

    def test_returns_true_with_valid_arguments(self):
        retval = restorepgsql_validate_options_and_args(
            self.options,
            []
            )
        self.assertTrue(retval)
