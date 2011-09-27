from tests.cmdline_test_skeleton import Cmdline_test_skeleton
from bbpgsql.configuration.repository import get_Snapshot_repository
from tests.archivepgsql_test.tar_archive_helpers import fill_directory_tree
from testfixtures import TempDirectory
from mock import patch
from bbpgsql.restore_pgsql import restorepgsql_handle_args
from bbpgsql.restore_pgsql import Restore_pgsql
#from bbpgsql.restore_pgsql import Restore_pgsql
#from bbpgsql.archive_pgsql import commit_pgsql_to_repository
import os.path
#import filecmp
#from bbpgsql.repository_exceptions import UnknownTagError
from subprocess import Popen, PIPE, STDOUT, check_call, CalledProcessError


class Test_restorepgsql(Cmdline_test_skeleton):
    __test__ = True  # to make nose run these tests
    exe_script = 'restorepgsql'

    def setup_environment_and_paths_customize(self):
        self.pgsql_data_dir = self.tempdir.makedir('datadir')
        self.snapshot_archive = self.tempdir.makedir('snapshotdir')
        self.test_data_dir = self.tempdir.makedir('testdir')
        self.file1_contents = 'some contents'
        self.file2_contents = 'other contents'
        self.filename1 = self.tempdir.write('file1', self.file1_contents)
        self.filename2 = self.tempdir.write('file2', self.file2_contents)
        pass

    def setup_config(self):
        self.config_dict = {
            'General': {
                'pgsql_data_directory': self.pgsql_data_dir,
            },
            'Snapshot': {
                'driver': 'filesystem',
                'path': self.snapshot_archive,
            },
            'WAL': {
                'driver': 'memory',
            },
        }
        return self.config_dict

    def setup_customize(self):
        self.repository = get_Snapshot_repository(self.config)
        fill_directory_tree(TempDirectory(path=self.test_data_dir))
        fill_directory_tree(TempDirectory(path=self.pgsql_data_dir))
        self.archive_cmd = ['archivepgsql', '--config', self.config_path]
        proc = Popen(
            self.archive_cmd,
            env=self.env,
            stdout=PIPE,
            stderr=STDOUT
            )
        proc.wait()

    def teardown_customize(self):
        pass

    def commit_filename1(self, tag, message=None):
        self.repository.create_commit_from_filename(
            tag,
            self.filename1,
            message
            )

    def commit_filename2(self, tag, message=None):
        self.repository.create_commit_from_filename(
            tag,
            self.filename2,
            message
            )

    def test_restorepgsql_raises_exception_if_destination_contains_data(self):

        def raises_exception():
            check_call(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)

        self.assertRaises(CalledProcessError, raises_exception)

    def test_data_in_destination_produces_proper_message(self):
        proc = Popen(self.cmd, env=self.env, stdout=PIPE, stderr=STDOUT)
        proc.wait()
        process_output = proc.stdout.read()
        print(process_output)
        self.assertTrue(
            'Data exists in PostgreSQL data directory.  Aborting restore'
            in process_output
            )

    @patch('bbpgsql.restore_pgsql.restorepgsql_validate_options_and_args')
    @patch('bbpgsql.restore_pgsql.restorepgsql_parse_args')
    def test_handle_args_calls_restorepgsql_parse_arg(
        self,
        mock_parse_args,
        mock_validate
        ):
        mock_parse_args.return_value = ('one', 'two', 'three')
        options, args = restorepgsql_handle_args()
        self.assertTrue(mock_parse_args.called)
        self.assertTrue(mock_validate.called)

    def test_Restore_pgsql_class_instantiation(self):
        restorer = Restore_pgsql(self.repository, self.pgsql_data_dir)
        self.assertEqual(restorer.repository, self.repository)
        self.assertEqual(restorer.data_dir, self.pgsql_data_dir)
        self.assertEqual(type(restorer.restore), type(self.setUp))

    def test_get_commit_to_restore_gets_last_commit(self):
        self.commit_filename1('a')
        self.commit_filename1('b')
        self.commit_filename1('c')
        self.commit_filename1('d')
        restorer = Restore_pgsql(self.repository, self.pgsql_data_dir)
        commit = restorer._get_commit_to_restore()
        self.assertEqual(commit.tag, 'd')
        self.commit_filename1('e')
        commit = restorer._get_commit_to_restore()
        self.assertEqual(commit.tag, 'e')

    def test_write_commit_to_temporary_storage_works(self):
        self.commit_filename1('a')
        self.commit_filename1('b')
        self.commit_filename2('c')
        commit = self.repository['c']
        r = Restore_pgsql(self.repository, self.pgsql_data_dir)
        r._write_commit_to_temporary_storage(commit, self.tempdir.path)
        filename = os.path.join(self.tempdir.path, 'snapshot.tar')
        fileobj = open(filename)
        self.assertEqual(self.file2_contents, fileobj.read())
'''
class Test_restorepgsql(Cmdline_test_skeleton):

    def setup_customize(self):
        self.setup_repository()
        self.restorer = Restore_WAL(self.repository)
        commit_wal_to_repository(self.repository, self.srcfilepath)
        self.basename = os.path.basename(self.srcfilepath)
        self.destfilepath = os.path.join(self.destdirpath, self.basename)

    def setup_repository(self):
        self.repository = get_WAL_repository(self.config)

    def setup_environment_and_paths_customize(self):
        self.srcfilepath = self.tempdir.write(
            os.path.join('source', 'WALFileName0001'),
            'Some Data goes here',
        )
        self.destdirpath = self.tempdir.makedir('destination')
        self.archivepath = self.tempdir.makedir('walarchive')

    def teardown_customize(self):
        self.teardown_tempdirs()

    def teardown_tempdirs(self):
        self.tempdir.cleanup()
'''
