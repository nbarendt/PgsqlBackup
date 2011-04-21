from sys import stdout
from bbpgsql.option_parser import common_parse_args
from bbpgsql.option_parser import common_validate_options_and_args

def archivepgsql_main():
    parser, options, args = common_parse_args()

    try:
        common_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(e)
        parser.print_help()
