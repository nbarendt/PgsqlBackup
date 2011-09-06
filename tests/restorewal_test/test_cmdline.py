from tests.cmdline_test_skeleton import Cmdline_test_skeleton
from bbpgsql.configuration.repository import get_WAL_repository
from bbpgsql.restore_wal import Restore_WAL
from bbpgsql.archive_wal import commit_wal_to_repository
import os.path
import filecmp
from bbpgsql.repository_exceptions import UnknownTagError


class Test_restorewal(Cmdline_test_skeleton):
    __test__ = True  # to make nose run these tests

    def setup_config(self):
        self.config_dict = {
            'General': {
                'pgsql_data_directory': self.destdirpath
            },
            'Snapshot': {
                'driver': 'memory',
            },
            'WAL': {
                'driver': 'memory',
            }
        }
        return self.config_dict

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

    def teardown_customize(self):
        self.teardown_tempdirs()

    def teardown_tempdirs(self):
        self.tempdir.cleanup()

    def null_test(self):
        pass

    def test_restorewal_sets_repository_attr(self):
        self.assertEqual(self.repository, self.restorer.repository)

    def test_restorewal_has_method_restore(self):
        self.assertEqual(type(self.restorer.restore), type(self.setUp))

    def test_restorewal_takes_two_arguments(self):
        self.restorer.restore(self.basename, self.destfilepath)

    def test_restorewal_restores_a_wal_file(self):
        self.restorer.restore(self.basename, self.destfilepath)
        self.assertTrue(filecmp.cmp(
            self.srcfilepath,
            self.destfilepath,
            shallow=False
            ))

    def test_restorewal_raises_unknown_tag_error(self):
        self.assertRaises(
            UnknownTagError,
            self.restorer.restore,
            'tag1',
            self.destfilepath
        )

'''
    Roadmap:

    going to need functionality that mirros archive_wal.  Two basic functions.
    1. restorewal_handle_args()
    2. restorewal_main()

    underneath need new function in option_parser to
    restorewal_validate_options_and_args()
'''
