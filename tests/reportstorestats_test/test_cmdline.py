from unittest import TestCase
from testfixtures import TempDirectory
import os
from subprocess import check_call


class Test_reportstorestats_BasicCommandLineOperation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'reportstorestats'

    def setUp(self):
        self.cmd = [self.exe_script]

    def tearDown(self):
        pass

    def test_reportstorestats_returns_error_if_given_an_argument(self):
        proc = check_call(self.cmd)
