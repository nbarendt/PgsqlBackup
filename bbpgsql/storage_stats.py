from sys import stdout, exit
from bbpgsql.option_parser import storagestats_parse_args
from bbpgsql.option_parser import storagestats_validate_options_and_args
from bbpgsql.configuration import get_config_from_filename
#from bbpgsql.configuration.repository import get_Snapshot_repository
#from bbpgsql.configuration.repository import get_WAL_repository


class Report_storage_stats(object):
    def __init__(self):
#        self.options, self.args = self.storagestats_handle_args()
#        selfconf = get_config_from_filename(self.options.config_file)
        self.topbottom_dashes = '{:-^76}\n'.format('')
        self.middle_dashes = '|{:-^74}|\n'.format('')
        self.item = '|{:^24}|{:>17} items |{:>20} MB |\n'
        self.column_headers = '|{:^24}|{:^24}|{:^24}|\n'.format(
            'Repository Name',
            'Number of Items',
            'Repository Size'
        )
#        self.WAL_repository = get_WAL_repository(self.conf)
#        self.snapshot_repo = get_Snapshot_repository(self.conf)
        self._filldata()

    def storagestats_handle_args(self):
        parser, options, args = storagestats_parse_args()

        try:
            storagestats_validate_options_and_args(options, args)
        except Exception, e:
            stdout.write(str(e) + '\n')
            parser.print_help()
            exit(1)
        return options, args

    def _filldata(self):
        total = 0
        repo_name = 'Snapshots'
        (items, size) = self._get_repository_size(repo_name)
        total += size
        self.snapshots = self.item.format(
            repo_name,
            '%s' % items,
            '%s' % size
        ) 
        repo_name = 'WAL Files'
        (items, size) = self._get_repository_size(repo_name)
        total += size
        self.walfiles = self.item.format(
            repo_name,
            '%s' % items,
            '%s' % size
        )
        self.total = '|{:^24} {:^24}|{:>20} MB |\n'.format(
            'Total Size',
            '',
            '%s' % total
        )

    def _get_repository_size(self, repo_name):
        if repo_name == 'Snapshots':
            return (100, 2000)
        if repo_name == 'WAL Files':
            return(1000, 1000)

    def write_report(self):
        stdout.write(self.topbottom_dashes)
        stdout.write(self.column_headers)
        stdout.write(self.middle_dashes)
        stdout.write(self.snapshots)
        stdout.write(self.walfiles)
        stdout.write(self.middle_dashes)
        stdout.write(self.total)
        stdout.write(self.topbottom_dashes)


def storagestats_main():
    reporter = Report_storage_stats()
    reporter.write_report()
    exit(0)

if __name__ == '__main__':
    storagestats_main()

#def dummy():
#    options, args = storagestats_handle_args()
#    conf = get_config_from_filename(options.config_file)
#    reporter = Report_storage_stats(conf)
#    reporter.write_report()

