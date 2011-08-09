from sys import stdout
from os.path import basename
from datetime import datetime
from bbpgsql.option_parser import archivewal_parse_args
from bbpgsql.option_parser import archivewal_validate_options_and_args
from bbpgsql.option_parser import get_wal_filename
from bbpgsql.configuration import get_config_from_filename_and_set_up_logging
from bbpgsql.configuration.repository import (
    get_WAL_repository
)
from bbpgsql.events import Support


def archivewal_handle_args():
    parser, options, args = archivewal_parse_args()

    try:
        archivewal_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(str(e) + '\n')
        parser.print_help()
        raise e
    return options, args


def archivewal_main():
    options, args = archivewal_handle_args()

    conf = get_config_from_filename_and_set_up_logging(options.config_file)

    wal_filename_to_archive = get_wal_filename(conf, args[0])

    repository = get_WAL_repository(conf)

    commit_wal_to_repository(repository, wal_filename_to_archive)


def commit_wal_to_repository(repository, wal_filename_to_archive):
    wal_basename = basename(wal_filename_to_archive)
    Support().notify_wal_started(wal_basename)
    repository.create_commit_from_filename(wal_basename,
        wal_filename_to_archive,
        datetime.utcnow().isoformat())
    Support().notify_wal_completed(wal_basename)
