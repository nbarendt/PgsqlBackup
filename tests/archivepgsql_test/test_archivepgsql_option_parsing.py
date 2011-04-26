from unittest import TestCase
from bbpgsql.option_parser import archivepgsql_parse_args
from bbpgsql.option_parser import archivepgsql_validate_options_and_args
from mock import patch, Mock


class Test_archivepgsql_parse_args_Uses_Common_Functions(TestCase):
    @patch('bbpgsql.option_parser.create_common_parser', spec=True)
    def test_create_common_parser_used(self, mock_func):
        mock_parser = Mock()
        mock_parser.parse_args.return_value = lambda: Mock(), []
        mock_func.return_value = mock_parser
        archivepgsql_parse_args(args=[])
        self.assertTrue(mock_func.called)

    @patch('bbpgsql.option_parser.create_common_parser', spec=True)
    def test_create_common_parser_passed_usage_string(self, mock_func):
        mock_parser = Mock()
        mock_parser.parse_args.return_value = lambda: Mock(), []
        mock_func.return_value = mock_parser
        archivepgsql_parse_args(args=[])
        kwargs = mock_func.call_args_list[0][1]
        expected_usage_suffix = '[options]'
        self.assertTrue(kwargs['usage'].endswith(expected_usage_suffix))


class Test_archivepgsql_validate_options_Uses_Common_Functions(TestCase):
    @patch('bbpgsql.option_parser.common_validate_options_and_args', spec=True)
    def test_will_call_common_validate_options_and_args(self, mock_func):
        mock_func.return_value = False
        archivepgsql_validate_options_and_args()
        self.assertTrue(mock_func.called)
