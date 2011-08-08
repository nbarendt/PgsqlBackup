#from unittest import TestCase
from subprocess import check_call
#from subprocess import Popen
from subprocess import PIPE
import os
#from copy import deepcopy
#from testfixtures import TempDirectory
#from mock import patch
from tests.cmdline_test_skeleton import Cmdline_test_skeleton
#from bbpgsql.configuration import get_config_from_filename_and_set_up_logging
#from bbpgsql.configuration import write_config_to_filename
#from bbpgsql.configuration.repository import get_Snapshot_repository
#import bbpgsql.archive_pgsql


class Test_archive_pgsql_logging(Cmdline_test_skeleton):
    __test__ = True  # to make nose run these tests
    LOG_FILE = 'bbpgsql.log'
    DATA_DIR = 'pgsql_data'
    ARCHIVE_DIR = 'pgsql_archive'

    exe_script = 'archivepgsql'

    def setup_environment_and_paths_customize(self):
        self.data_dir = self.tempdir.makedir(self.DATA_DIR)
        self.archive_dir = self.tempdir.makedir(self.ARCHIVE_DIR)
        self.log_file = os.path.join(self.tempdir.path, self.LOG_FILE)

    def setup_config(self):
        self.config_dict = {
            'General': {
                'pgsql_data_directory': self.data_dir,
            },
            'Snapshot': {
                'driver': 'memory',
            },
            'Logging': {
                'logfile': self.log_file,
                'level': 'INFO',
            },
        }
        return self.config_dict

    def setup_customize(self):
        pass

    def teardown_customize(self):
        pass

    def test_archive_pgsql_logs_success_at_INFO(self):
        check_call(self.cmd, env=self.env, stdout=PIPE)
        log = open(self.log_file)
        expected = 'archive_pgsql executed successfully\n'
        self.assertEqual(expected, log.read())
        assert False
