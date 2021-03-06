import os
import stat
from optparse import OptionParser
from bbpgsql.configuration import get_config_from_filename_and_set_up_logging
from bbpgsql.configuration.general import get_data_dir
from subprocess import check_output
import sys

VERSION = ''


class BadArgumentException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class TooManyArgumentsException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NotEnoughArgumentsException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class UsedArchivepgsqlAsArchiveWAL(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def get_version():
    # override "version" with a constant string for release
    version = VERSION or check_output(['git', 'describe']).strip()
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
    if not os.access(options.config_file, os.R_OK):
        raise Exception("No read access for %s" % (options.config_file))
    config_stats = os.stat(options.config_file)
    if ((config_stats.st_mode & stat.S_IRWXG) |
        (config_stats.st_mode & stat.S_IRWXO)):
        raise Exception("File %s has open group or other permissions" %
            (options.config_file))
    return True


def non_destructive_minimal_parse_and_validate_args(args=None):
    args = args or sys.argv[:]
    parser, options, args = common_parse_args(args)
    common_validate_options_and_args(options, args)
    return options, args


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
    config = get_config_from_filename_and_set_up_logging(options.config_file)
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
    if args:
        if args[0].startswith('pg_xlog'):
            raise UsedArchivepgsqlAsArchiveWAL('archivepgsql was called with' \
                            ' a WAL file path as an argument.  This is' \
                            ' probably due to configuring archivepgsql' \
                            ' as the archive_command in the PGSQL' \
                            ' configuration instead of archivewal.')
        raise TooManyArgumentsException('archivepgsql should not be called' \
                        ' with any arguments.  Are you using it as the' \
                        ' archive_command instead of archivewal?')
    return True


def restorewal_parse_args(args=None):
    restorewal_usage = ' '.join([
        os.path.basename(sys.argv[0]),
        '[options]',
        '<name_of_wal_file_to_restore>',
        '<path_to_write_restored_file>',
        ])
    parser = create_common_parser(usage=restorewal_usage)
    options, args = parser.parse_args(args)
    return parser, options, args


def restorewal_validate_options_and_args(options=None, args=None):
    args = args or []
    if not common_validate_options_and_args(options, args):
        return False
    nargs = len(args)
    if nargs != 2:
        raise Exception('restorewal must be given the name of the WAL' \
                        ' file to retrieve and the destination path to' \
                        ' restore to.')
    return True


def storagestats_parse_args(args=None):
    storagestats_usage = ' '.join([
        os.path.basename(sys.argv[0]),
        '[options]'])
    parser = create_common_parser(usage=storagestats_usage)
    options, args = parser.parse_args(args)
    return parser, options, args


def storagestats_validate_options_and_args(options=None, args=None):
    if not common_validate_options_and_args(options, args):
        return False
    if args:
        raise TooManyArgumentsException('storagestats takes no arguments')
    return True
