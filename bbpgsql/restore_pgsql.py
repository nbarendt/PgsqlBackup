from bbpgsql.option_parser import (
    restorepgsql_parse_args,
    restorepgsql_validate_options_and_args
)
from sys import stdout
from bbpgsql.configuration import get_config_from_filename_and_set_up_logging
from bbpgsql.configuration.general import get_data_dir


class Restore_pgsql(object):
    def __init__(self, repository, data_dir):
        self.repository = repository
        self.data_dir = data_dir
        self.latest_snapshot = repository

    def restore(self):
        pass


def restorepgsql_handle_args():
    parser, options, args = restorepgsql_parse_args()
    try:
        restorepgsql_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(str(e) + '\n')
        parser.print_help()
        raise e
    return options, args


def restorepgsql_main():
    options, args = restorepgsql_handle_args()
    conf = get_config_from_filename_and_set_up_logging(options.config_file)
    repository = get_Snapshot_repository(conf)
    data_dir = get_data_dir(conf)


if __name__ == '__main__':
    restorepgsql_main()
