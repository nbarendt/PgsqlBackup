from unittest import TestCase
from subprocess import check_call
import os
from copy import deepcopy
from testfixtures import TempDirectory


class Test_archivepgsql_BasicCommandLineOperation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'archivepgsql'

    def setUp(self):
        self.setup_environment()
        self.setup_config()
        self.cmd = [self.exe_script, '--config', self.config_path]

    def setup_environment(self):
        self.env = deepcopy(os.environ)
        self.env['PATH'] = ''.join([
            self.env['PATH'],
            ':',
            self.ARCHIVEPGSQL_PATH])
        self.tempdir = TempDirectory()

    def setup_config(self):
        self.config_path = self.tempdir.write(self.CONFIG_FILE, '')

    def tearDown(self):
        self.tempdir.cleanup()

    def test_can_execute_archivepgsql(self):
        check_call(self.cmd, env=self.env)
