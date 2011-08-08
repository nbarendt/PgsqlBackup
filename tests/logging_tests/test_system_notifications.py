from unittest import TestCase
from testfixtures import LogCapture
from bbpgsql.events import Support


class Test_notification_logs_message(TestCase):
    def setUp(self):
        self.support = Support()

    def test_notification_logs_message(self):
        with LogCapture() as l:
            self.support.notify_null()
            l.check(('root', 'INFO', ''))

    def test_snapshot_started_logs_message(self):
        with LogCapture() as l:
            tag = '1234'
            wal1 = '456'
            self.support.notify_snapshot_started(tag, wal1)
            expected_msg = 'Backup snapshot started (%s) (%s:)' % (
                tag, wal1)
            l.check(('root', 'INFO', expected_msg))

    def test_snapshot_complete_logs_message(self):
        with LogCapture() as l:
            tag = '1234'
            wal1 = '456'
            wal2 = '789',
            self.support.notify_snapshot_completed(tag, wal1, wal2)
            expected_msg = 'Backup snapshot completed (%s) (%s:%s)' % (
                tag, wal1, wal2)
            l.check(('root', 'INFO', expected_msg))

    def test_wal_started_logs_message(self):
        with LogCapture() as l:
            wal = '1234'
            self.support.notify_wal_started(wal)
            expected_msg = 'WAL file archive started (%s)' % (wal)
            l.check(('root', 'INFO', expected_msg))

    def test_wal_complete_logs_message(self):
        with LogCapture() as l:
            wal = '456'
            self.support.notify_wal_completed(wal)
            expected_msg = 'WAL file archive completed (%s)' % (wal)
            l.check(('root', 'INFO', expected_msg))
