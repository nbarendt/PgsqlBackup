from nose.tools import *
from unittest import TestCase
from subprocess import check_call
import os
from copy import deepcopy

class Test_archivepgsql_BasicCommandLineOperation(object):
    ARCHIVEPGSQL_PATH=os.path.join('PgsqlBackup', 'cmdline_scripts')
    cmd = 'archivepgsql'

    def setup(self):
        self.env = deepcopy(os.environ)
        self.env['PATH'] = ''.join([self.env['PATH'],
            ':',
            self.ARCHIVEPGSQL_PATH])

    def test_can_execute_archivepgsql(self):
       check_call([self.cmd], env=self.env)
