from unittest import TestCase
#from testfixtures import TempDirectory
import os
from sys import stdout
from copy import deepcopy
import subprocess
from bbpgsql.storage_stats import Report_storage_stats


class Test_reportstorestats_BasicCommandLineOperation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'storagestats'

    def setUp(self):
        self.setup_environment()
        self.cmd = [self.exe_script]
        self.num_snapshots = 100
        self.size_snapshots = 2000
        self.num_walfiles = 1000
        self.size_walfiles = 1000
        self.topbottom_dashes = '{:-^76}\n'.format('')
        self.middle_dashes = '|{:-^74}|\n'.format('')
        self.column_headers = '|{:^24}|{:^24}|{:^24}|\n'.format(
            'Repository Name',
            'Number of Items',
            'Repository Size'
        )
        self.item = '|{:^24}|{:>17} items |{:>20} MB |\n'
        self.snapshots = self.item.format(
            'Snapshots',
            '%s' % self.num_snapshots,
            '%s' % self.size_snapshots
        )
        self.walfiles = self.item.format(
            'WAL Files',
            '%s' % self.num_walfiles,
            '%s' % self.size_walfiles
        )
        self.total = '|{:^24} {:^24}|{:>20} MB |\n'.format(
            'Total Size',
            '',
            '3000'
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
        stdout.write(self.expected_output)
        stdout.write(output)
        self.assertEqual(self.expected_output, output)

    def test_get_repository_size_returns_snapshot_data(self):
        rss = Report_storage_stats()
        (items, size) = rss._get_repository_size('Snapshots')
        self.assertEqual(items, self.num_snapshots)
        self.assertEqual(size, self.size_snapshots)

    def test_get_repository_size_returns_walfile_data(self):
        rss = Report_storage_stats()
        (items, size) = rss._get_repository_size('WAL Files')
        self.assertEqual(items, self.num_walfiles)
        self.assertEqual(size, self.size_walfiles)
