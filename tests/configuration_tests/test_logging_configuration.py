from unittest import TestCase
from nose.plugins.skip import SkipTest
from mock import patch
from testfixtures import TempDirectory
from bbpgsql.configuration import (
    config,
    set_up_logging,
    set_up_logger_file_handler,
    set_up_logger_syslog_handler,
)
#import logging
#import logging.config
#import logging.handlers
import os.path
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
logfile=/needs/setting/in/setUp/bbpgsql
loghistory=14
loghost=localhost
logport=514
'''

config_bad_values = '''
[Logging]
level=DORK
logfile=/nonexistent/path
loghistory=not_a_number
loghost=nohost
logport=not_a_number
'''


class Test_Logging_setup(TestCase):
    def setUp(self):
        self.default_config = config()
        self.td = TempDirectory()
        self.logdir = self.td.makedir('log')
        self.logfilepath = os.path.join(self.logdir, 'bbpgsql')
        self.config_path = self.td.write('bbpgsql', config_text)
        self.full_config = config([self.config_path])
        self.full_config.set('Logging', 'logfile', self.logfilepath)
        self.config_path = self.td.write('bad_level', config_bad_values)
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
    def test_logger_sets_log_level_from_configfile(self, mock_setLevel):
        set_up_logging(self.full_config)
        self.assertEqual(2, mock_setLevel.call_count)
        expected = ((DEBUG, ), {})
        self.assertEqual(expected, mock_setLevel.call_args)

    @patch('logging.Logger.setLevel')
    def test_logger_rejects_bad_level_name(self, mock_setLevel):
        self.assertRaises(Exception, set_up_logging, (self.bad_config))
        self.assertEqual(1, mock_setLevel.call_count)

    @patch('logging.Logger.addHandler')
    @patch('logging.handlers.TimedRotatingFileHandler')
    def test_logger_gets_filename_from_config(
        self,
        mock_TRFH,
        mock_logger_addHandler
    ):
        set_up_logger_file_handler(self.full_config)
        self.assertEqual(1, mock_logger_addHandler.call_count)
        self.assertEqual(1, mock_TRFH.call_count)
        expected = (
            (self.logfilepath, ),
            {'backupCount': 14, 'interval': 1, 'when': 'd'}
        )
        self.assertEqual(expected, mock_TRFH.call_args)

    @patch('logging.Logger.addHandler')
    @patch('logging.handlers.TimedRotatingFileHandler')
    def test_logger_does_nothing_if_logfile_not_defined(
        self,
        mock_TRFH,
        mock_logger_addHandler,
    ):
        set_up_logger_file_handler(self.default_config)
        self.assertFalse(mock_logger_addHandler.called)
        self.assertFalse(mock_TRFH.called)

    @patch('logging.Logger.addHandler')
    @patch('logging.handlers.SysLogHandler')
    def test_logger_gets_hostname_port_from_config(
        self,
        mock_SLH,
        mock_logger_addHandler,
    ):
        set_up_logger_syslog_handler(self.full_config)
        self.assertEqual(1, mock_logger_addHandler.call_count)
        self.assertEqual(1, mock_SLH.call_count)
        expected = ((), {'address': ('localhost', 514)})
        self.assertEqual(expected, mock_SLH.call_args)

    @patch('logging.Logger.addHandler')
    @patch('logging.handlers.SysLogHandler')
    def test_logger_does_nothing_if_syslog_host_not_defined(
        self,
        mock_SLH,
        mock_logger_addHandler,
    ):
        set_up_logger_syslog_handler(self.default_config)
        self.assertEqual(0, mock_logger_addHandler.call_count)
        self.assertEqual(0, mock_SLH.call_count)

    @patch('bbpgsql.configuration.set_up_logger_file_handler')
    @patch('bbpgsql.configuration.set_up_logger_syslog_handler')
    def test_set_up_logging_calls_handler_setups(
        self,
        mock_set_up_logger_syslog_handler,
        mock_set_up_logger_file_handler,
    ):
        set_up_logging(self.full_config)
        self.assertEqual(1, mock_set_up_logger_file_handler.call_count)
        self.assertEqual(1, mock_set_up_logger_syslog_handler.call_count)

    @patch('bbpgsql.configuration.set_up_logger_file_handler')
    @patch('bbpgsql.configuration.set_up_logger_syslog_handler')
    def test_set_up_logging_does_not_setup_handlers_if_no_logging_section(
        self,
        mock_set_up_logger_syslog_handler,
        mock_set_up_logger_file_handler,
    ):
        set_up_logging(self.default_config)
        self.assertEqual(0, mock_set_up_logger_file_handler.call_count)
        self.assertEqual(0, mock_set_up_logger_syslog_handler.call_count)
