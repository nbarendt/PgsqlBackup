from sys import stdout, exit

class Report_storage_stats(object):
    def init(self):
        self.topbottom_dashes = '{:-^76}'.format('')
        self.middle_dashes = '|{:-^74}|'.format('')
        self.total = '|{:<24} {:^24}|{:>24}|'.format(
            'Total Size',
            '',
            '3000 MB'
        )
        self.column_headers = '|{:^24}|{:^24}|{:^24}|'.format(
            'Repository Name',
            'Number of Items',
            'Repository Size'
        )
        self.snapshots = '|{:^24}|{:^24}|{:^24}|'.format(
            'Snapshots',
            '100',
            '2000 MB'
        ) 
        self.walfiles = '|{:^24}|{:^24}|{:^24}|'.format(
            'WAL Files',
            '1000',
            '1000 MB'
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

def reportstorestats_main(self):
    rss = Report_storage_stats()
    rss.init()
    rss.write_report()
    exit(0)
