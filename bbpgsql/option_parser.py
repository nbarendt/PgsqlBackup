import os
import stat
from optparse import OptionParser
from bbpgsql.configuration import get_config_from_filename
from bbpgsql.configuration.general import get_data_dir
from subprocess import check_output
import sys

class BadArgumentException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def get_version():
    # override "version" with a constant string for release
    version = "0.1.0" #check_output(['git', 'describe']).strip()
    return ' '.join(['%prog', version])
    
def create_common_parser(**kwargs):
    kwargs['version'] = get_version()
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
    config_stats = os.stat(options.config_file)
    if ((config_stats.st_mode & stat.S_IRWXG) |
        (config_stats.st_mode & stat.S_IRWXO)):
        raise Exception("File %s has open group or other permissions" %
            (options.config_file))
    return True


def archivewal_parse_args(args=None):
    archivewal_usage = ' '.join([
        os.path.basename(sys.argv[0]),
       '[options]',
        '<path_to_wal_file_to_archive>'])
    parser = create_common_parser(usage=archivewal_usage)
    options, args = parser.parse_args(args)
    return parser, options, args


def is_relative_path(wal_path):
    return not os.path.isabs(wal_path)

def wal_file_exists(config, wal_path):
    return os.path.isfile(get_wal_filename(config, wal_path))

def get_wal_filename(config, wal_path):
    data_dir = get_data_dir(config)
    return os.path.join(data_dir, wal_path)

def is_valid_file(config, wal_path):
    return is_relative_path(wal_path) and wal_file_exists(config, wal_path)


def archivewal_validate_options_and_args(options=None, args=None):
    args = args or []
    if not common_validate_options_and_args(options, args):
        return False
    config = get_config_from_filename(options.config_file)
    if len(args) != 1 or not is_valid_file(config, args[0]):
        raise Exception('A relative path to a WAL file to be archived' \
                        ' must be provided!')
    return True

def archivepgsql_parse_args(args=None):
    archivepgsql_usage = ' '.join([
        os.path.basename(sys.argv[0]),
       '[options]'])
    parser = create_common_parser(usage=archivepgsql_usage)
    options, args = parser.parse_args(args)
    return parser, options, args

def archivepgsql_validate_options_and_args(options=None, args=None):
    if not common_validate_options_and_args(options, args):
        return False
    return True

