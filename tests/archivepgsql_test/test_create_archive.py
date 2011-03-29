from unittest import TestCase
import os
from testfixtures import TempDirectory
from bbpgsql.create_archive import create_archive

class Test_archive_create(TestCase):
    def setUp(self):
        self.srcDir = TempDirectory()
        self.destDir = TempDirectory()
        self.archiveName = 'archive.tar'
        self.archivePath = os.path.join(self.destDir.path, self.archiveName)

    def tearDown(self):
        self.srcDir.cleanup()
        self.destDir.cleanup()

    def test_can_create_archive_file(self):
        create_archive(self.srcDir.path, self.destDir.path, self.archiveName)
        self.fh = open(self.archivePath)

