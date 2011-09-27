from bbpgsql.option_parser import (
    restorepgsql_parse_args,
    restorepgsql_validate_options_and_args
)
from sys import stdout
from bbpgsql.configuration import get_config_from_filename_and_set_up_logging
from bbpgsql.configuration.general import get_data_dir
from bbpgsql.configuration.repository import get_Snapshot_repository
from bbpgsql.temporarydirectory import TemporaryDirectory
from bbpgsql.extract_archive import extract_archive
import os.path


class Restore_pgsql(object):
    def __init__(self, repository, data_dir):
        self.repository = repository
        self.data_dir = data_dir
        self.latest_snapshot = repository

    def restore(self):
        with TemporaryDirectory(suffix='restorepgsql') as tempdir:
            commit = self._get_commit_to_restore()
            filename = self._write_commit_to_temporary_storage(commit, tempdir)
            self._extract_commit_to_data_dir(filename)

    def _get_commit_to_restore(self):
        tags = self.repository.keys()
        return self.repository[tags[-1]]

    def _write_commit_to_temporary_storage(self, commit, tempdir):
        tempfile = os.path.join(tempdir, 'snapshot.tar')
        commit.get_contents_to_filename(tempfile)
        return tempfile

    def _extract_commit_to_data_dir(self, filename):
        extract_archive(filename, self.data_dir)


def restorepgsql_handle_args():
    parser, options, args = restorepgsql_parse_args()
    try:
        restorepgsql_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(str(e) + '\n')
        parser.print_help()
        raise e
    return options, args


def restorepgsql_main():
    options, args = restorepgsql_handle_args()
    conf = get_config_from_filename_and_set_up_logging(options.config_file)
    repository = get_Snapshot_repository(conf)
    data_dir = get_data_dir(conf)
    restorer = Restore_pgsql(repository, data_dir)
    restorer.restore()


if __name__ == '__main__':
    restorepgsql_main()
