from sys import stdout, exit
from os.path import basename
from datetime import datetime
from bbpgsql.option_parser import archivewal_parse_args
from bbpgsql.option_parser import archivewal_validate_options_and_args
from bbpgsql.configuration import get_config_from_filename
from bbpgsql.configuration.repository import (
    get_WAL_repository
)


def archivewal_handle_args():
    parser, options, args = archivewal_parse_args()

    try:
        archivewal_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(str(e) + '\n')
        parser.print_help()
        exit(1)
    return options, args


def archivewal_main():
    options, args = archivewal_handle_args()

    wal_filename_to_archive = args[0]

    conf = get_config_from_filename(options.config_file)

    repository = get_WAL_repository(conf)

    commit_wal_to_repository(repository, wal_filename_to_archive)


def commit_wal_to_repository(repository, wal_filename_to_archive):
    wal_basename = basename(wal_filename_to_archive)
    repository.create_commit_from_filename(wal_basename,
        wal_filename_to_archive,
        datetime.utcnow().isoformat())