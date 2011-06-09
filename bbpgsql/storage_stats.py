from sys import stdout, exit
from bbpgsql.option_parser import storagestats_parse_args
from bbpgsql.option_parser import storagestats_validate_options_and_args
from bbpgsql.configuration import get_config_from_filename
from bbpgsql.configuration.repository import get_Snapshot_repository
from bbpgsql.configuration.repository import get_WAL_repository


class Storage_stats_reporter(object):
    ONE_MEBIBYTE = 1024. * 1024.


    def __init__(self, repo_names, repositories):
        self.repo_names = repo_names
        self.repositories = repositories
        self.repo_sizes = {}
        self.topbottom_dashes = '{:-^76}\n'.format('')
        self.middle_dashes = '|{:-^74}|\n'.format('')
        self.item = '|{:^24}|{:>17} items |{:>20} MB |\n'
        self.column_headers = '|{:^24}|{:^24}|{:^24}|\n'.format(
            'Item Category',
            'Number of Items',
            'Size of All Items'
        )
        self.total_templ = '|{:^24} {:^24}|{:>20} MB |\n'
        self.firstlast_templ = '|{:^24}|{:^49}|\n'

    def _filldata(self):
        total = 0
        for repo_name, repo in self.repositories.iteritems():
            items, size = self._get_repository_size(repo)
            total += size
            self.repo_sizes[repo_name] = self.item.format(
                repo_name,
                '%s' % items,
                '%s' % (size / self.ONE_MEBIBYTE)
            )
        self.total = self.total_templ.format(
            'Total Size',
            '',
            '%s' % (total / self.ONE_MEBIBYTE)
        )
        self.first_ss, self.last_ss = self._get_first_and_last_commit_tags(
            self.repositories[self.repo_names[0]]
        )
        self.first = self.firstlast_templ.format(
            'First Snapshot:',
            self.first_ss
        )
        self.last = self.firstlast_templ.format(
            'Last Snapshot:',
            self.last_ss
        )

    def _get_repository_size(self, repo):
        items = repo.get_number_of_items()
        size = repo.get_repository_size()
        return items, size

    def _get_first_and_last_commit_tags(self, repo):
        all = [c for c in repo]
        if len(all):
            return all[0].tag, all[-1].tag
        else:
            return 'Repository Empty', 'No Commits'

    def write_report(self, stream):
        self._filldata()
        stream.write(self.topbottom_dashes)
        stream.write(self.column_headers)
        stream.write(self.middle_dashes)
        for name in self.repo_names:
            stream.write(self.repo_sizes[name])
        stream.write(self.middle_dashes)
        stream.write(self.total)
        stream.write(self.middle_dashes)
        stream.write(self.first)
        stream.write(self.last)
        stream.write(self.topbottom_dashes)


def storagestats_main():
    options, args = storagestats_handle_args()
    conf = get_config_from_filename(options.config_file)
    repo_names = [ 'Snapshots', 'WAL Files' ]
    repositories = {
        repo_names[0]: get_Snapshot_repository(conf),
        repo_names[1]: get_WAL_repository(conf),
    }
    reporter = Storage_stats_reporter(repo_names, repositories)
    reporter.write_report(stdout)
    exit(0)

def storagestats_handle_args():
    parser, options, args = storagestats_parse_args()

    try:
        storagestats_validate_options_and_args(options, args)
    except Exception, e:
        stdout.write(str(e) + '\n')
        parser.print_help()
        exit(1)
    return options, args

if __name__ == '__main__':
    storagestats_main()

#def dummy():
#    options, args = storagestats_handle_args()
#    conf = get_config_from_filename(options.config_file)
#    reporter = Storage_stats_reporter(conf)
#    reporter.write_report()

