from sys import stdout
from bbpgsql.option_parser import archivepgsql_parse_args
from bbpgsql.option_parser import archivepgsql_validate_options_and_args
from bbpgsql.configuration import get_config_from_filename
from bbpgsql.configuration.general import get_data_dir
from bbpgsql.configuration.repository import get_Snapshot_repository
from bbpgsql.pg_backup_control import pg_start_backup
from bbpgsql.pg_backup_control import pg_stop_backup
from bbpgsql.create_archive import create_archive
from datetime import datetime
from re import match
from tempfile import mkdtemp, template
from shutil import rmtree
from os.path import exists, join


def archivepgsql_handle_args():
    parser, options, args = archivepgsql_parse_args()

    try:
        archivepgsql_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(str(e) + '\n')
        parser.print_help()
        exit(1)
    return options, args

# borrowing from Python 3
class TemporaryDirectory:
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everthing contained
    in it are removed.
    """

    def __init__(self, suffix="", prefix=template, dir=None):
        self.name = mkdtemp(suffix, prefix, dir)

    def __enter__(self):
        return self.name

    def cleanup(self):
        if exists(self.name):
            rmtree(self.name)

    def __exit__(self, exc, value, tb):
        self.cleanup()

def archivepgsql_main():
    options, args = archivepgsql_handle_args()
    conf = get_config_from_filename(options.config_file)
    data_dir = get_data_dir(conf)

    with TemporaryDirectory(suffix='archivepgsql') as tempdir:
        tag = generate_tag()
        archive_dst_path = join(tempdir, 'pgsql.snapshot.tar')
        repo = get_Snapshot_repository(conf)
        if options.dry_run:
            print("Dry Run")
            return
        else:
            perform_backup(data_dir, archive_dst_path, tag, repo)

def perform_backup(src_dir, archivefile, tag, repo):
    print("This is perform_backup")
    first_WAL = pg_start_backup(tag)
    create_archive(src_dir, archivefile)
    second_WAL = pg_stop_backup()
    commit_snapshot_to_repository(repo, archivefile, tag, first_WAL, second_WAL)

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
   
