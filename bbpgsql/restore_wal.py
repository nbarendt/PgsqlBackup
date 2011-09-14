from sys import stdout
from bbpgsql.configuration.repository import get_WAL_repository
from bbpgsql.option_parser import restorewal_parse_args
from bbpgsql.option_parser import restorewal_validate_options_and_args
from bbpgsql.configuration import get_config_from_filename_and_set_up_logging


class Restore_WAL(object):
    def __init__(self, repository):
        self.repository = repository

    def restore(self, basename, destination):
        commit = self.repository[basename]
        commit.get_contents_to_filename(destination)


def restorewal_handle_args():
    parser, options, args = restorewal_parse_args()

    try:
        restorewal_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(str(e) + '\n')
        parser.print_help()
        raise e
    return options, args


def restorewal_main():
    options, args = restorewal_handle_args()

    conf = get_config_from_filename_and_set_up_logging(options.config_file)

    repository = get_WAL_repository(conf)

    restorer = Restore_WAL(repository)
    restorer.restore(args[0], args[1])
