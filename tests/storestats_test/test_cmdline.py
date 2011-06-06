from unittest import TestCase

class Test_reportstorestats_BasicCommandLineOperation(TestCase):
    ARCHIVEPGSQL_PATH = os.path.join('bbpgsql', 'cmdline_scripts')
    CONFIG_FILE = 'config.ini'
    exe_script = 'reportstorestats'

    def setUp(self):
        pass

    def tearDown(self):
        pass
