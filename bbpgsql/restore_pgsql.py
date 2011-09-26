from bbpgsql.option_parser import (
    restorepgsql_parse_args,
    restorepgsql_validate_options_and_args
)
from sys import stdout


class Restore_pgsql(object):
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
    restorepgsql_handle_args()


if __name__ == '__main__':
    restorepgsql_main()
