from unittest import TestCase
#from testfixtures import TempDirectory
import os
from copy import deepcopy
import subprocess


class Test_reportstorestats_BasicCommandLineOperation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'storagestats'

    def setUp(self):
        self.setup_environment()
        self.cmd = [self.exe_script]
        self.topbottom_dashes = '{:-^76}\n'.format('')
        self.middle_dashes = '|{:-^74}|\n'.format('')
        self.total = '|{:^24} {:^24}|{:>24}|\n'.format(
            'Total Size',
            '',
            '3000 MB '
        )
        self.column_headers = '|{:^24}|{:^24}|{:^24}|\n'.format(
            'Repository Name',
            'Number of Items',
            'Repository Size'
        )
        self.snapshots = '|{:^24}|{:>24}|{:>24}|\n'.format(
            'Snapshots',
            '100 items ',
            '2000 MB '
        )
        self.walfiles = '|{:^24}|{:>24}|{:>24}|\n'.format(
            'WAL Files',
            '1000 items ',
            '1000 MB '
        )
        self.expected_output = ''.join([
            self.topbottom_dashes,
            self.column_headers,
            self.middle_dashes,
            self.snapshots,
            self.walfiles,
            self.middle_dashes,
            self.total,
            self.topbottom_dashes,
        ])

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
