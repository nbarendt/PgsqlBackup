from unittest import TestCase
from bbpgsql.option_parser import common_parse_args
from bbpgsql.option_parser import create_common_parser
from bbpgsql.option_parser import common_validate_options_and_args
from bbpgsql.configuration import write_config_to_filename
from testfixtures import TempDirectory
from re import match
import os
import stat


class Test_CommandLineOptionParsing_Defaults(TestCase):
    def setUp(self):
        self.parser, self.options, self.args = common_parse_args(args=[])

    def test_can_parse_empty_command_line(self):
        self.assertTrue(self.options)

    def test_not_dry_run_by_default(self):
        self.assertFalse(self.options.dry_run)

    def test_uses_etc_config_file_by_default(self):
        self.assertEqual('/etc/bbpgsql.ini', self.options.config_file)


class Test_CommandLineOptionParsing_Versioning(TestCase):
    def test_can_get_version_provided_to_parser_constructor(self):
        parser = create_common_parser()
        version_regex = r'^nosetests\s+v(\d+)\.(\d+)\.(\d+)'
        version = parser.get_version()
        print "version_regex", version_regex
        print "version", version
        self.assertTrue(match(version_regex, version))


class Test_CommandLineOptionParsing_With_Options(TestCase):
    def setUp(self):
        self.config_path = '/tmp/blah/blah/bbpgsql.ini'
        args = ['--dry-run', '--config', self.config_path]
        self.parser, self.options, self.args = common_parse_args(args=args)

    def test_override_config_file(self):
        self.assertEqual(self.config_path, self.options.config_file)

    def test_can_execute_dry_run(self):
        self.assertTrue(self.options.dry_run)


class Test_OptionParsing_and_Validation(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.config_dict = {
        }
        self.config_path = os.path.join(self.tempdir.path, 'config.ini')
        write_config_to_filename(self.config_dict, self.config_path)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_validation_raises_exception_if_config_file_does_not_exist(self):
        def validate():
            parser, options, args = common_parse_args(args=[
                '--config', '/tmp/blah/blah/bbpgsql.ini'])
            common_validate_options_and_args(options, args)
        self.assertRaises(Exception, validate)

    def test_validation_raises_exception_if_config_file_permissions_too_open(
        self):
        with TempDirectory() as d:
            self.parent_dir = d.makedir('parent_dir')
            self.config_path = d.write('parent_dir/config.ini', '')
            self.open_perm = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO
            os.chmod(self.config_path, self.open_perm)
            def validate(config_path):
                parser, options, args = common_parse_args(args=[
                    '--config', config_path])
                common_validate_options_and_args(options, args)
            self.assertRaises(Exception, validate, self.config_path)

    def test_options_validate_if_config_file_exists(self):
        parser, options, args = common_parse_args(args=[
            '--config', self.config_path])
        self.assertTrue(common_validate_options_and_args(options, args))
