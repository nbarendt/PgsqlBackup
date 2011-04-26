from sys import stdout
from bbpgsql.option_parser import common_parse_args
from bbpgsql.option_parser import common_validate_options_and_args
from datetime import datetime
from re import match

def archivepgsql_main():
    parser, options, args = common_parse_args()

    try:
        common_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(e)
        parser.print_help()

    # need to do something like:
    #  tag = generate_tag()
    #  first_WAL = pg_start_backup
    #  tar magic 
    #  second_WAL = pg_stop_backup
    #  commit_snapshot_to_repository(repo, tarfile, tag, first_wal, last_wal)
    

def generate_tag():
   return datetime.utcnow().isoformat() 

def commit_snapshot_to_repository(repo, snapshot_filename, tag, first_WAL,
    last_WAL):
    repo.create_commit_from_filename(tag, snapshot_filename,
        _generate_message_from_WAL_filenames(first_WAL, last_WAL))

def _generate_message_from_WAL_filenames(first_WAL, last_WAL):
    return 'firstWAL:{0}-lastWAL:{1}'.format(first_WAL, last_WAL)

def _get_WAL_filenames_from_message(message):
    print message
    m = match(r"firstWAL:([^\-]+)-lastWAL:([^\-]+)", message)
    return m.group(1), m.group(2)

def get_first_WAL(repo, tag):
    message = repo[tag].message 
    return _get_WAL_filenames_from_message(message)[0]

def get_last_WAL(repo, tag):
    message = repo[tag].message 
    return _get_WAL_filenames_from_message(message)[1]
   
