from os.path import basename
from sys import stdout, exit
from bbpgsql.archive_wal import archivewal_main
from bbpgsql.archive_pgsql import archivepgsql_main
from bbpgsql.storage_stats import storagestats_main
from bbpgsql.option_parser import (
    non_destructive_minimal_parse_and_validate_args)
from bbpgsql.configuration import get_config_from_filename_and_set_up_logging
import logging

#PYINSTALLER KLUDGES
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
MIMEMultipart
MIMEBase
MIMEText


def bbpgsql_error():
    msg = '''You have invoked this script as bbpgsql.
This script is supposed to be invoked through the commands archivepgsql
and archivewal.  Please check with your adminstrator to make sure these
commands were installed correctly.
'''
    stdout.write(msg)
    exit(1)


def get_dispatch_map():
    CMD_DISPATCH_MAP = {
        'archivewal': archivewal_main,
        'archivepgsql': archivepgsql_main,
        'storagestats': storagestats_main,
        'bbpgsql': bbpgsql_error,
    }
    return CMD_DISPATCH_MAP


def bbpgsql_main(argv):
    cmd_name = basename(argv[0])
    dispatch_map = get_dispatch_map()
    if cmd_name in dispatch_map:
        options, args = non_destructive_minimal_parse_and_validate_args(argv)
        get_config_from_filename_and_set_up_logging(options.config_file)
        try:
            dispatch_map[cmd_name]()
        except Exception, e:
            logging.error(str(e))
            logging.shutdown()
            raise e 
    else:
        stdout.write('Unknown command: {0}\n'.format(cmd_name))
        exit(1)
