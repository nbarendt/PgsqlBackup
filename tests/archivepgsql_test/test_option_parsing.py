from nose.tools import *
from unittest import TestCase
from bbpgsql.option_parser import parse_args
from testfixtures import TempDirectory

class Test_CommandLineOptionParsing(TestCase):

    def setUp(self):
        self.tempdir = TempDirectory()
        self.config_path = self.tempdir.write('config.ini', '')

    def tearDown(self):
        self.tempdir.cleanup()

    def test_can_parse_empty_command_line(self):
        assert self.tempdir
        assert self.config_path
        self.assertTrue(parse_args(args=['test_app',
            '--config', self.config_path])[0])
