import os
from optparse import OptionParser


def common_parse_args(args=None):
    parser = OptionParser()

    parser.add_option('-c', '--config', dest='config_file',
        help='configuration file', default='/etc/bbpgsql.ini')

    parser.add_option('--dry-run', dest='dry_run',
        help='test run - do not actually modify any files',
        action='store_true',
        default=False)

    return parser.parse_args(args)


def common_validate_options_and_args(options=None, args=None):
    if not os.path.exists(options.config_file):
        raise Exception("File %s does not exist" % (options.config_file))

    return True
