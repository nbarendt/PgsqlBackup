from unittest import TestCase
from mock import patch
from testfixtures import TempDirectory
from bbpgsql.configuration import (
    config,
    set_up_logging,
    set_up_logger_file_handler,
)
from bbpgsql.configuration.general import (
    get_data_dir,
    MissingDataDirError,
    )
import logging
import os.path


class Test_General_data_dir(TestCase):
    def setUp(self):
        self.config = config()

    def test_will_raise_MissingDataDirError(self):

        def will_raise_MissingDataDirError():
            get_data_dir(self.config)

        self.assertRaises(MissingDataDirError,
            will_raise_MissingDataDirError)


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
class Test_Logging(TestCase):
    def setUp(self):
        self.log_conf = {
        }
        self.tmpdir = TempDirectory()
        self.logfile = os.path.join(self.tmpdir.path, 'bbpgsql')

    def tearDown(self):
        pass

    def test_logger_bbpgsql(self):
        mylog = logging.getLogger()
        l = set_up_logging()
        self.assertEqual(type(mylog), type(l))
        print((type(mylog), type(l)))

    @patch('logging.getLogger')
    def test_set_up_logger_calls_getLogger(self, mock_getLogger):
        set_up_logging()
        self.assertTrue(mock_getLogger.called)

    def test_handler_file(self):
        myfh = logging.handlers.TimedRotatingFileHandler(self.logfile)
        fh = set_up_logger_file_handler(self.logfile)
        print((type(myfh), type(fh)))
        self.assertEqual(type(myfh), type(fh))

    @patch('logging.handlers.TimedRotatingFileHandler')
    def test_set_up_logger_file_handler(self, mock_trfh):
        set_up_logger_file_handler(self.logfile)
        self.assertTrue(mock_trfh.called)
