import logging


class Support(object):
    def notify_null(self):
        logging.info('')

    def notify_snapshot_started(self, tag, wal1):
        logging.info('Backup snapshot started (%s) (%s:)' % (tag, wal1))

    def notify_snapshot_completed(self, tag, wal1, wal2):
        logging.info('Backup snapshot completed (%s) (%s:%s)' % (
            tag, wal1, wal2))

    def notify_wal_started(self, wal):
        logging.info('WAL file archive started (%s)' % (wal))

    def notify_wal_completed(self, wal):
        logging.info('WAL file archive completed (%s)' % (wal))
