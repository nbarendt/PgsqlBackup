from unittest import TestCase
from testfixtures import TempDirectory
import os
from copy import deepcopy
from bbpgsql.configuration import get_config_from_filename
from bbpgsql.configuration import write_config_to_filename


class Cmdline_test_skeleton(TestCase):
    __test__ = False  # to prevent nose from running this skeleton
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    ONE_MEBIBYTE = 1024. * 1024.
    ONE_MEGABYTE = 1000. * 1000.

    exe_script = 'fill this in with your command'

    def setUp(self):
        self.setup_environment()
        self.write_config_to_disk()
        self.cmd = [self.exe_script, '--config', self.config_path]
        self.setup_customize()

    def setup_customize(self):
        raise Exception('This is a skeleton for test - you need to provide'
                        'your own customization function, setup_customize')

    def setup_environment(self):
        self.env = deepcopy(os.environ)
        self.env['PATH'] = ''.join([
            self.env['PATH'],
            ':',
            self.ARCHIVEPGSQL_PATH])
        self.tempdir = TempDirectory()

    def write_config_to_disk(self):
        self.config_path = os.path.join(self.tempdir.path, self.CONFIG_FILE)
        write_config_to_filename(self.setup_config(), self.config_path)
        self.config = get_config_from_filename(self.config_path)

    def tearDown(self):
        self.teardown_customize()

    def teardown_customize(self):
        raise Exception('This is a skeleton for test - you need to provide'
                        'your own customization function, teardown_customize')
