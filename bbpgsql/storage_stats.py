from sys import stdout, exit

class Report_storage_stats(object):
    def __init__(self):
        self.topbottom_dashes = '{:-^76}\n'.format('')
        self.middle_dashes = '|{:-^74}|\n'.format('')
        self.item = '|{:^24}|{:>17} items |{:>20} MB |\n'
        self.column_headers = '|{:^24}|{:^24}|{:^24}|\n'.format(
            'Repository Name',
            'Number of Items',
            'Repository Size'
        )
        self.filldata()

    def filldata(self):
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

    def _write_report(self):
        stdout.write(self.topbottom_dashes)
        stdout.write(self.column_headers)
        stdout.write(self.middle_dashes)
        stdout.write(self.snapshots)
        stdout.write(self.walfiles)
        stdout.write(self.middle_dashes)
        stdout.write(self.total)
        stdout.write(self.topbottom_dashes)

def storagestats_main():
    rss = Report_storage_stats()
    rss._write_report()
    exit(0)

if __name__ == '__main__':
    storagestats_main()
