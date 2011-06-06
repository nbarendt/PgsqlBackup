from unittest import TestCase
#from testfixtures import TempDirectory
import os
from copy import deepcopy
import subprocess


class Test_reportstorestats_BasicCommandLineOperation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'reportstorestats'

    def setUp(self):
        self.setup_environment()
        self.cmd = [self.exe_script]
        self.expected_output = '''
                 Repository         # of items      Repository size 
'''

    def setup_environment(self):
        self.env = deepcopy(os.environ)
        self.env['PATH'] = ''.join([
            self.env['PATH'],
            ':',
            self.ARCHIVEPGSQL_PATH])

    def tearDown(self):
        pass

    def test_reportstorestats_returns_proper_report(self):
        output = subprocess.check_output(
            [self.exe_script],
            env=self.env,
            stderr=subprocess.STDOUT)
        self.assertEqual(self.expected_output, output)
