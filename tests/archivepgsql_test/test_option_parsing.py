from unittest import TestCase
from bbpgsql.option_parser import parse_args
from testfixtures import TempDirectory


class Test_CommandLineOptionParsing(TestCase):

    def test_can_parse_empty_command_line(self):
        options, args = parse_args(args=[])
        self.assertTrue(options)

    def test_uses_etc_config_file_by_default(self):
        options, args = parse_args(args=[])
        self.assertEqual('/etc/bbpgsql.ini', options.config_file)

    def test_override_config_file(self):
        config_path = '/tmp/blah/blah/bbpgsql.ini'
        options, args = parse_args(args=['--config', config_path])
        self.assertEqual(config_path, options.config_file)

    def test_not_dry_run_by_default(self):
        options, args = parse_args(args=[])
        self.assertFalse(options.dry_run)

    def test_can_execute_dry_run(self):
        options, args = parse_args(args=['--dry-run'])
        self.assertTrue(options.dry_run) 


class Test_OptionParsing_and_Validation(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.config_path = self.tempdir.write('config.ini', '')

    def tearDown(self):
        self.tempdir.cleanup()

    def test_config_file_must_exist(self):
        config_path = '/tmp/blah/blah/bbpgsql.ini'
        options, args = parse_args(args=['--config', config_path])
        self.assertEqual(config_path, options.config_file)
