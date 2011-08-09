from configuration import BBPGSQL_LOGGER_NAME
import logging


def get_logger():
    return logging.getLogger(BBPGSQL_LOGGER_NAME)


class Support(object):
    def notify_null(self):
        get_logger().info('')

    def notify_snapshot_started(self, tag, wal1):
        get_logger().info('Backup snapshot started (%s) (%s:)' % (tag, wal1))

    def notify_snapshot_completed(self, tag, wal1, wal2):
        get_logger().info('Backup snapshot completed (%s) (%s:%s)' % (
            tag, wal1, wal2))

    def notify_wal_started(self, wal):
        get_logger().info('WAL file archive started (%s)' % (wal))

    def notify_wal_completed(self, wal):
        get_logger().info('WAL file archive completed (%s)' % (wal))
