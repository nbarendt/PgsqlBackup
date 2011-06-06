from sys import stdout, exit

class Report_storage_stats(object):
    def init(self):
        self.topbottom_dashes = '{:-^76}\n'.format('')
        self.middle_dashes = '|{:-^74}|\n'.format('')
        self.total = '|{:^24} {:^24}|{:>24}|\n'.format(
            'Total Size',
            '',
            '3000 MB '
        )
        self.column_headers = '|{:^24}|{:^24}|{:^24}|\n'.format(
            'Repository Name',
            'Number of Items',
            'Repository Size'
        )
        self.snapshots = '|{:^24}|{:>24}|{:>24}|\n'.format(
            'Snapshots',
            '100 items ',
            '2000 MB '
        ) 
        self.walfiles = '|{:^24}|{:>24}|{:>24}|\n'.format(
            'WAL Files',
            '1000 items ',
            '1000 MB '
        )

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
    rss = Report_storage_stats()
    rss.init()
    rss.write_report()
    exit(0)

if __name__ == '__main__':
    storagestats_main()
