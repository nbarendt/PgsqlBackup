from unittest import TestCase
from unittest import skip
from testfixtures import TempDirectory
from mock import Mock
import os
from sys import stdout
from copy import deepcopy
#import subprocess
import StringIO
from bbpgsql.storage_stats import Storage_stats_reporter
from bbpgsql.configuration import get_config_from_filename
from bbpgsql.configuration import write_config_to_filename
from bbpgsql.configuration.repository import get_Snapshot_repository
from bbpgsql.configuration.repository import get_WAL_repository


class Test_storagestats_skeleton(TestCase):
    __test__ = False # to prevent nose from running this skeleton

    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'storagestats'
    ONE_MEBIBYTE = 1024. * 1024.

    def setUp(self):
        self.setup_environment()
        self.setup_config()
        self.setup_repositories()
        self.setup_report()
        self.cmd = [self.exe_script, '--config', self.config_path]

    def setup_environment(self):
        self.env = deepcopy(os.environ)
        self.env['PATH'] = ''.join([
            self.env['PATH'],
            ':',
            self.ARCHIVEPGSQL_PATH])
        self.tempdir = TempDirectory()

    def setup_config(self):
        self.config_path = os.path.join(self.tempdir.path, self.CONFIG_FILE)
        self.config_dict = {
            'General': {
            },
            'Snapshot': {
                'driver': 'memory',
            },
            'WAL': {
                'driver': 'memory',
            }
        }
        write_config_to_filename(self.config_dict, self.config_path)
        self.config = get_config_from_filename(self.config_path)


class Test_storestats_with_real_repos(Test_storagestats_skeleton):
    __test__ = True # to make nose run these tests

    def setup_repositories(self):
        self.repo_names = [ 'Snapshots', 'WAL Files' ]
        self.repositories = {
            self.repo_names[0]: get_Snapshot_repository(self.config),
            self.repo_names[1]: get_WAL_repository(self.config),
        }
        self.num_snapshots = 0
        self.num_walfiles = 0
        self.size_snapshots = 0
        self.size_walfiles = 0

    def setup_report(self):
        self.topbottom_dashes = '{:-^76}\n'.format('')
        self.middle_dashes = '|{:-^74}|\n'.format('')
        self.column_headers = '|{:^24}|{:^24}|{:^24}|\n'.format(
            'Item Category',
            'Number of Items',
            'Size of All Items'
        )
        self.item = '|{:^24}|{:>17} items |{:>20} MB |\n'
        self.snapshots = self.item.format(
            self.repo_names[0],
            '%s' % self.num_snapshots,
            '%s' % (self.size_snapshots / self.ONE_MEBIBYTE)
        )
        self.walfiles = self.item.format(
            self.repo_names[1],
            '%s' % self.num_walfiles,
            '%s' % (self.size_walfiles / self.ONE_MEBIBYTE)
        )
        self.size_total = self.size_snapshots + self.size_walfiles
        self.total_templ = '|{:^24} {:^24}|{:>20} MB |\n'
        self.total = self.total_templ.format(
            'Total Size',
            '',
            '%s' % (self.size_total / self.ONE_MEBIBYTE)
        )
        self.firstlast_templ = '|{:^24}|{:^49}|\n'
        self.first = self.firstlast_templ.format(
            'First Snapshot:',
            'Repository Empty'
        )
        self.last = self.firstlast_templ.format(
            'Last Snapshot:',
            'No Commits'
        )
        self.expected_output_lines = [
            self.topbottom_dashes,
            self.column_headers,
            self.middle_dashes,
            self.snapshots,
            self.walfiles,
            self.middle_dashes,
            self.total,
            self.middle_dashes,
            self.first,
            self.last,
            self.topbottom_dashes,
        ]
        self.expected_output = ''.join(self.expected_output_lines)

    def tearDown(self):
        pass

    def test_get_snapshots_size_empty_repository(self):
        rss = Storage_stats_reporter(self.repo_names, self.repositories)
        (items, size) = rss._get_repository_size(
            self.repositories[self.repo_names[0]]
        )
        self.assertEqual(0, items)
        self.assertEqual(0, size)

    def test_get_walfiles_size_empty_repository(self):
        rss = Storage_stats_reporter(self.repo_names, self.repositories)
        (items, size) = rss._get_repository_size(
            self.repositories[self.repo_names[1]]
        )
        self.assertEqual(0, items)
        self.assertEqual(0, size)

    def test_write_report_empty_repository(self):
        rss = Storage_stats_reporter(self.repo_names, self.repositories)
        myout = StringIO.StringIO()
        rss.write_report(myout)
        output = myout.getvalue()
        print(output)
        #assert False
        myout.close()
        stdout.write(self.expected_output)
        stdout.write(output)
        self.assertEqual(self.expected_output, output)

    def commit_a_file(self, repo, file, contents, tag, message):
        filename = self.tempdir.write(file, contents)
        repo.create_commit_from_filename(tag, filename, message)

    def fill_repositories_with_commits(self):
        repo_ss = self.repositories[self.repo_names[0]]
        repo_wal = self.repositories[self.repo_names[1]]
        self.commit_a_file(repo_ss, 'file1', 'contents1', 'TAG001', 'Message1')
        self.commit_a_file(repo_ss, 'file2', 'contents2', 'TAG002', 'Message2')
        self.commit_a_file(repo_ss, 'file3', 'contents3', 'TAG003', 'Message3')
        self.commit_a_file(repo_ss, 'file4', 'contents4', 'TAG004', 'Message4')
        self.commit_a_file(repo_wal, 'file1', 'contents1', 'TAG001', 'Message1')
        self.commit_a_file(repo_wal, 'file2', 'contents2', 'TAG002', 'Message2')
        self.commit_a_file(repo_wal, 'file3', 'contents3', 'TAG003', 'Message3')
        self.commit_a_file(repo_wal, 'file4', 'contents4', 'TAG004', 'Message4')
        self.commit_a_file(repo_wal, 'file5', 'contents5', 'TAG005', 'Message5')
        self.commit_a_file(repo_wal, 'file6', 'contents6', 'TAG006', 'Message6')
        self.commit_a_file(repo_wal, 'file7', 'contents7', 'TAG007', 'Message7')
        self.commit_a_file(repo_wal, 'file8', 'contents8', 'TAG008', 'Message8')

    def test_get_repository_size_with_items(self):
        repo_ss = self.repositories[self.repo_names[0]]
        repo_wal = self.repositories[self.repo_names[1]]
        self.fill_repositories_with_commits()
        rss = Storage_stats_reporter(self.repo_names, self.repositories)
        num_items, size_items = rss._get_repository_size(repo_ss)
        self.assertEqual(
            repo_ss.get_number_of_items(),
            num_items
        )
        self.assertEqual(
            repo_ss.get_repository_size(),
            size_items
        )
        num_items, size_items = rss._get_repository_size(repo_wal)
        self.assertEqual(
            repo_wal.get_number_of_items(),
            num_items
        )
        self.assertEqual(
            repo_wal.get_repository_size(),
            size_items
        )

    def test_get_first_and_last_snapshot(self):
        repo_ss = self.repositories[self.repo_names[0]]
        self.fill_repositories_with_commits()
        rss = Storage_stats_reporter(self.repo_names, self.repositories)
        all_comm = [c for c in repo_ss]
        first_comm = all_comm[0].tag
        last_comm = all_comm[-1].tag
        first, last = rss._get_first_and_last_commit_tags(repo_ss)
        print(first_comm, first)
        print(last_comm, last)
        self.assertEqual(first_comm, first)
        self.assertEqual(last_comm, last)

    def test_filled_repository_produces_correct_output(self):
        repo_ss = self.repositories[self.repo_names[0]]
        repo_wal = self.repositories[self.repo_names[1]]
        self.fill_repositories_with_commits()
        self.num_snapshots = repo_ss.get_number_of_items()
        self.size_snapshots = repo_ss.get_repository_size()
        self.num_walfiles = repo_wal.get_number_of_items()
        self.size_walfiles = repo_wal.get_repository_size()
        total = self.size_snapshots + self.size_walfiles
        self.snapshots = self.item.format(
            self.repo_names[0],
            '%s' % self.num_snapshots,
            '%s' % (self.size_snapshots / self.ONE_MEBIBYTE)
        )
        self.walfiles = self.item.format(
            self.repo_names[1],
            '%s' % self.num_walfiles,
            '%s' % (self.size_walfiles / self.ONE_MEBIBYTE)
        )
        self.total = self.total_templ.format(
            'Total Size',
            '',
            '%s' % (total / self.ONE_MEBIBYTE)
        )
        all = [c for c in repo_ss]
        self.first = self.firstlast_templ.format(
            'First Snapshot:',
            all[0].tag
        )
        self.last = self.firstlast_templ.format(
            'Last Snapshot:',
            all[-1].tag
        )
        self.expected_output_lines = [
            self.topbottom_dashes,
            self.column_headers,
            self.middle_dashes,
            self.snapshots,
            self.walfiles,
            self.middle_dashes,
            self.total,
            self.middle_dashes,
            self.first,
            self.last,
            self.topbottom_dashes,
        ]
        self.expected_output = ''.join(self.expected_output_lines)
        rss = Storage_stats_reporter(self.repo_names, self.repositories)
        myout = StringIO.StringIO()
        rss.write_report(myout)
        output = myout.getvalue()
        print(output)
        myout.close()
        stdout.write(self.expected_output)
        stdout.write(output)
        self.assertEqual(self.expected_output, output)
