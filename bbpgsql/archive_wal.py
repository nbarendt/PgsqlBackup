import os
from datetime import datetime


def commit_wal_to_repository(repository, wal_filename_to_archive):
    wal_basename = os.path.basename(wal_filename_to_archive)
    repository.create_commit_from_filename(wal_basename,
        wal_filename_to_archive,
        datetime.utcnow().isoformat())
