from os.path import basename
from sys import stdout, exit
from bbpgsql.archive_wal import archivewal_main
from bbpgsql.archive_pgsql import archivepgsql_main

#PYINSTALLER KLUDGES
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
MIMEMultipart
MIMEBase
MIMEText

def bbpgsql_error():
    pass

def get_dispatch_map():
    CMD_DISPATCH_MAP = {
        'archivewal': archivewal_main,
        'archivepgsql': archivepgsql_main,
        'bbpgsql': bbpgsql_error,
    }
    return CMD_DISPATCH_MAP

def bbpgsql_main(argv):
    cmd_name = basename(argv[0])
    dispatch_map = get_dispatch_map()
    if cmd_name in dispatch_map:
        dispatch_map[cmd_name]()
    else:
        stdout.write('Unknown command: {0}\n'.format(cmd_name))
        exit(1)
