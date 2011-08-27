from unittest import TestCase
from mock import patch
from testfixtures import TempDirectory
import bbpgsql.configuration
import os.path
from ConfigParser import SafeConfigParser
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
    'formatters': {
    },
    'loggers': {
        'bbpgsql': {
            'handlers': [],
        },
    },
}

config_only_section = '''
[Logging]
'''

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
        self.default_config = bbpgsql.configuration.config()
        self.td = TempDirectory()
        self.logdir = self.td.makedir('log')
        self.logfilepath = os.path.join(self.logdir, 'bbpgsql')
        self.config_path = self.td.write('bbpgsql', config_text)
        self.full_config = bbpgsql.configuration.config([self.config_path])
        self.full_config.set('Logging', 'logfile', self.logfilepath)
        self.config_path = self.td.write('bad_level', config_bad_values)
        self.bad_config = bbpgsql.configuration.config([self.config_path])
        self.config_path = self.td.write('section_only', config_only_section)
        self.section_only = bbpgsql.configuration.config([self.config_path])

    def tearDown(self):
        self.td.cleanup()

    def test_default_config_lacks_logging(self):
        self.assertFalse(self.default_config.has_section('Logger'))

    def test_section_only_does_no_logging(self):
        log_config = bbpgsql.configuration.set_up_logging(self.section_only)
        # assert only null handler
        self.assertEqual(1, len(log_config['handlers']))

    @patch('logging.config.dictConfig')
    def test_logger_sets_up_default_config(self, mock_dictConfig):
        mock_dictConfig.return_value = None
        bbpgsql.configuration.set_up_logging(self.default_config)
        self.assertTrue(mock_dictConfig.called)
        expected = ((default_log_config, ), {})
        self.assertEqual(expected, mock_dictConfig.call_args)

    def test_logger_sets_log_level_from_configfile(self):
        log_config = bbpgsql.configuration.set_up_logging(self.full_config)
        self.assertEqual(DEBUG,
            log_config['loggers']['bbpgsql']['level'])

    def test_logger_rejects_bad_level_name(self):
        self.assertRaises(Exception, bbpgsql.configuration.set_up_logging,
            (self.bad_config))

    def test_logger_gets_filename_from_config(self):
        handlers, formatters = \
            bbpgsql.configuration.set_up_logger_file_handler(self.full_config)
        self.assertEqual(handlers,
            {'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'file_formatter',
                'filename': self.logfilepath,
                'when': 'd',
                'interval': 1,
                'backupCount': 14
                }
            }
        )
        self.assertEqual(formatters,
            {
                'file_formatter': {
                'format': "%(asctime)s - %(levelname)s - %(message)s",
                }
            }
        )

    def test_logger_does_nothing_if_section_is_missing(self):
        handlers, formatters = \
            bbpgsql.configuration.set_up_logger_file_handler(
                self.default_config)
        self.assertEqual({}, handlers)
        self.assertEqual({}, formatters)

    def test_logger_gets_hostname_port_from_config(self):
        handlers, formatters = \
            bbpgsql.configuration.set_up_logger_syslog_handler(
                self.full_config)
        self.assertEqual(handlers['syslog']['address'],
            ('localhost', 514))

    def test_logger_does_nothing_if_syslog_host_not_defined(self):
        conf = SafeConfigParser()
        conf.add_section('Logging')
        conf.set('Logging', 'logport', '514')
        handlers, formatters = \
            bbpgsql.configuration.set_up_logger_syslog_handler(conf)
        self.assertEqual({}, handlers)
        self.assertEqual({}, formatters)

    def test_logger_does_nothing_if_syslog_port_not_defined(self):
        conf = SafeConfigParser()
        conf.add_section('Logging')
        conf.set('Logging', 'loghost', 'localhost')
        handlers, formatters = \
            bbpgsql.configuration.set_up_logger_syslog_handler(conf)
        self.assertEqual({}, handlers)
        self.assertEqual({}, formatters)

    @patch('bbpgsql.configuration.set_up_logger_file_handler')
    @patch('bbpgsql.configuration.set_up_logger_syslog_handler')
    def test_set_up_logging_calls_handler_setups(
        self,
        mock_set_up_logger_syslog_handler,
        mock_set_up_logger_file_handler,
    ):
        mock_set_up_logger_syslog_handler.return_value = ({}, {})
        mock_set_up_logger_file_handler.return_value = ({}, {})
        log_config = bbpgsql.configuration.set_up_logging(self.full_config)
        from pprint import pprint
        pprint(log_config)
        self.assertEqual(1, mock_set_up_logger_file_handler.call_count)
        self.assertEqual(1, mock_set_up_logger_syslog_handler.call_count)

    @patch('bbpgsql.configuration.set_up_logger_file_handler')
    @patch('bbpgsql.configuration.set_up_logger_syslog_handler')
    def test_set_up_logging_does_not_setup_handlers_if_no_logging_section(
        self,
        mock_set_up_logger_syslog_handler,
        mock_set_up_logger_file_handler,
    ):
        bbpgsql.configuration.set_up_logging(self.default_config)
        self.assertEqual(0, mock_set_up_logger_file_handler.call_count)
        self.assertEqual(0, mock_set_up_logger_syslog_handler.call_count)
