from unittest import TestCase
from testfixtures import LogCapture
import logging
from bbpgsql.events import get_logger


class Test_basic_logging(TestCase):

    def test_root_logger(self):
        with LogCapture() as l:
            logging.info('test')
            l.check(('root', 'INFO', 'test'))

    def test_logger_name_is_as_expected(self):
        self.assertEqual('bbpgsql', get_logger().name)
