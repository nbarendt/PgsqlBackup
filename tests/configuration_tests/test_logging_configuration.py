from unittest import TestCase
from nose.plugins.skip import SkipTest
from mock import patch
from testfixtures import TempDirectory
from bbpgsql.configuration import (
    config,
    set_up_logging,
)
#import logging
#import logging.config
#import logging.handlers
#import os.path
from logging import (
    DEBUG,
#    INFO,
    WARNING,
#    ERROR,
#    CRITICAL,
)


default_log_config = {
    'version': 1,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'level': WARNING,
        'handlers': ['null'],
    },
}


config_text = '''
[Logging]
level=DEBUG
'''

config_bad_level = '''
[Logging]
level=DORK
'''


class Test_Logging_setup(TestCase):
    def setUp(self):
        self.default_config = config()
        self.td = TempDirectory()
        self.config_path = self.td.write('bbpgsql', config_text)
        self.full_config = config([self.config_path])
        self.config_path = self.td.write('bad_level', config_bad_level)
        self.bad_config = config([self.config_path])

    def tearDown(self):
        self.td.cleanup()

    def test_default_config_lacks_logging(self):
        self.assertFalse(self.default_config.has_section('Logger'))

    @patch('logging.config.dictConfig')
    def test_logger_sets_up_default_config(self, mock_dictConfig):
        mock_dictConfig.return_value = None
        set_up_logging(self.default_config)
        self.assertTrue(mock_dictConfig.called)
        expected = ((default_log_config, ), {})
        self.assertEqual(expected, mock_dictConfig.call_args)

    @patch('logging.Logger.setLevel')
    def test_logger_sets_warn_level_from_configfile(self, mock_setLevel):
        set_up_logging(self.full_config)
        self.assertEqual(2, mock_setLevel.call_count)
        print(mock_setLevel.call_count, mock_setLevel.call_args)
        expected = ((DEBUG, ), {})
        self.assertEqual(expected, mock_setLevel.call_args)

    @patch('logging.Logger.setLevel')
    def test_logger_rejects_bad_level_name(self, mock_setLevel):
        raise(SkipTest)
        set_up_logging(self.bad_config)
        self.assertEqual(1, mock_setLevel.call_count)

#  Logging Psuedo code outline
#
#  Create a default configuration dictionary in the module
#
#  set up logging
#    get default dict
#    modify default dict with values from main config file
#    instantiate logger from dict
#
#  Questions:
#  Must default have all the keys already?
#  Can config file add new keys to dict?
#  Must default dict values be valid?
#  Required values in main config are:
#    syslog host  Default?
#    syslog port  Default?
#    log directory  Default = /var/log
#    number of days of history to keep around  Default = 7 days
#    log level  Default = warn
