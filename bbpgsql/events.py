import logging

logger = logging.getLogger()

class Support(object):
    def notify_null(self):
        logger.info('')

    def notify_snapshot_started(self, tag, wal1):
        logger.info('Backup snapshot started (%s) (%s:)' % (tag, wal1))

    def notify_snapshot_completed(self, tag, wal1, wal2):
        logger.info('Backup snapshot completed (%s) (%s:%s)' % (
            tag, wal1, wal2))

    def notify_wal_started(self, wal):
        logger.info('WAL file archive started (%s)' % (wal))

    def notify_wal_completed(self, wal):
        logger.info('WAL file archive completed (%s)' % (wal))
