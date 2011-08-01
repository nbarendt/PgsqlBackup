from unittest import TestCase
from testfixtures import TempDirectory
import os
import stat
from bbpgsql.configuration import get_config_from_filename_and_set_up_logging
from bbpgsql.configuration import write_config_to_filename


class Test_write_config_to_filename(TestCase):
    def setUp(self):
        self.test_configuration = {
            'Test Section': {
                'Test_key': 'Test_value',
            },
        }

    def tearDown(self):
        pass

    def test_write_config_to_filename(self):
        with TempDirectory() as d:
            config_filename = os.path.join(d.path, 'config.ini')
            write_config_to_filename(self.test_configuration, config_filename)
            config = get_config_from_filename_and_set_up_logging(
                config_filename
            )
            self.assertEqual('Test_value',
                config.get('Test Section', 'Test_key'))

    def test_file_written_with_closed_permissions(self):
        with TempDirectory() as d:
            config_filename = os.path.join(d.path, 'config.ini')
            write_config_to_filename(self.test_configuration, config_filename)
            file_stats = os.stat(config_filename)
            self.assertFalse(file_stats.st_mode & stat.S_ISUID)
            self.assertFalse(file_stats.st_mode & stat.S_ISGID)
            self.assertFalse(file_stats.st_mode & stat.S_ISVTX)
            self.assertFalse(file_stats.st_mode & stat.S_IRWXG)
            self.assertFalse(file_stats.st_mode & stat.S_IRWXO)
