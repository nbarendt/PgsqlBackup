from bbpgsql.option_parser import (
    restorepgsql_parse_args,
    restorepgsql_validate_options_and_args
)


class Restore_pgsql(object):
    pass


def restorepgsql_handle_args():
    parser, options, args = restorepgsql_parse_args()
    restorepgsql_validate_options_and_args(options, args)


def restorepgsql_main():
    raise Exception(
        'Data exists in PostgreSQL data directory.  Aborting restore'
        )
