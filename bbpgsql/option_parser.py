import os
from optparse import OptionParser
import sys


class BadArgumentException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def create_common_parser(**kwargs):
    parser = OptionParser(**kwargs)

    parser.add_option('-c', '--config', dest='config_file',
        help='configuration file', default='/etc/bbpgsql.ini')

    parser.add_option('--dry-run', dest='dry_run',
        help='test run - do not actually modify any files',
        action='store_true',
        default=False)

    return parser


def common_parse_args(args=None):
    parser = create_common_parser()
    options, args = parser.parse_args(args)
    return parser, options, args


def common_validate_options_and_args(options=None, args=None):
    if not os.path.exists(options.config_file):
        raise Exception("File %s does not exist" % (options.config_file))
    return True


def archivewal_parse_args(args=None):
    archivewal_usage = ' '.join([
        os.path.basename(sys.argv[0]),
       '[options]',
        '<path_to_wal_file_to_archive>'])
    parser = create_common_parser(usage=archivewal_usage)
    options, args = parser.parse_args(args)
    return parser, options, args

def is_valid_file(wal_path):
    return os.path.isabs(wal_path) and os.path.isfile(wal_path)

def archivewal_validate_options_and_args(options=None, args=None):
    if not common_validate_options_and_args(options, args):
        return False
    if len(args) != 1 or not is_valid_file(args[0]):
        raise Exception('An absolute path to a WAL file to be archived' \
                        ' must be provided!')
    return True
