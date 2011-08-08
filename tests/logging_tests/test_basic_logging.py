from unittest import TestCase
from testfixtures import LogCapture
import logging


class Test_basic_logging(TestCase):

    def test_root_logger(self):
        with LogCapture() as l:
            logging.info('test')
            l.check(('root', 'INFO', 'test'))
