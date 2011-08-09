from unittest import TestCase
from mock import Mock
from testfixtures import LogCapture
import bbpgsql.archive_wal


class Test_log_events(TestCase):
    def test_wal_archive_emits_log_messages(self):
        expected_started = 'WAL file archive started (null)'
        expected_completed = 'WAL file archive completed (null)'
        with LogCapture() as l:
            bbpgsql.archive_wal.commit_wal_to_repository(
                Mock(),
                '/dev/null')
            l.check(
                ('bbpgsql', 'INFO', expected_started),
                ('bbpgsql', 'INFO', expected_completed)
            )
