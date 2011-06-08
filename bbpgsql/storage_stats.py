from sys import stdout, exit
from bbpgsql.option_parser import storagestats_parse_args
from bbpgsql.option_parser import storagestats_validate_options_and_args
from bbpgsql.configuration import get_config_from_filename
from bbpgsql.configuration.repository import get_Snapshot_repository
from bbpgsql.configuration.repository import get_WAL_repository


class Storage_stats_reporter(object):
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
        self._filldata()

    def _filldata(self):
        total = 0
        for repo_name, repo in self.repositories.iteritems():
            items, size = self._get_repository_size(repo_name, repo)
            total += size
            self.repo_sizes[repo_name] = self.item.format(
                repo_name,
                '%s' % items,
                '%s' % size
            )
        self.total = '|{:^24} {:^24}|{:>20} MB |\n'.format(
            'Total Size',
            '',
            '%s' % total
        )

    def _get_repository_size(self, repo_name, repo):
        items = repo.get_number_of_items()
        size = repo.get_repository_size()
        return items, size
        if repo_name == 'Snapshots':
            return (100, 2000)
        if repo_name == 'WAL Files':
            return(1000, 1000)
        else:
            print("Hey!  UnKnown repo name!!!!")

    def write_report(self, stream):
        stream.write(self.topbottom_dashes)
        stream.write(self.column_headers)
        stream.write(self.middle_dashes)
        for name in self.repo_names:
            stream.write(self.repo_sizes[name])
        stream.write(self.middle_dashes)
        stream.write(self.total)
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

