from tests.cmdline_test_skeleton import Cmdline_test_skeleton
from bbpgsql.configuration.repository import get_WAL_repository
from bbpgsql.restore_wal import Restore_WAL


class Test_restorewal(Cmdline_test_skeleton):
    __test__ = True  # to make nose run these tests
    config_dict = {
        'General': {
        },
        'Snapshot': {
            'driver': 'memory',
        },
        'WAL': {
            'driver': 'memory',
        }
    }

    def setup_config(self):
        return self.config_dict

    def setup_customize(self):
        self.setup_repository()
        self.setup_tempdirs()

    def setup_repository(self):
        self.repository = get_WAL_repository(self.config)

    def setup_tempdirs(self):
        pass

    def teardown_customize(self):
        self.teardown_tempdirs()

    def teardown_tempdirs(self):
        pass

    def null_test(self):
        pass

    def test_restorewal_sets_repository_attr(self):
        restorer = Restore_WAL(self.repository)
        self.assertEqual(self.repository, restorer.repository)

    def test_restorewal_has_method_restore(self):
        restorer = Restore_WAL(self.repository)
        self.assertEqual(type(restorer.restore), type(self.setUp))

    def test_restorewal_takes_two_arguments(self):
        restorer = Restore_WAL(self.repository)
        restorer.restore('one', 'two')
