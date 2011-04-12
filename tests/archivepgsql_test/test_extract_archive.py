from unittest import TestCase
#from nose.plugins.skip import SkipTest
#import os
#import tarfile
import filecmp
from bbpgsql.create_archive import create_archive
from bbpgsql.extract_archive import extract_archive
from tar_archive_helpers import create_valid_source_and_destination_paths
from tar_archive_helpers import create_invalid_source_and_destination_paths
from tar_archive_helpers import cleanup_temporary_directories
from tar_archive_helpers import fill_directory_tree


class Test_archive_extract(TestCase):
    def setUp(self):
        create_valid_source_and_destination_paths(self)
        create_invalid_source_and_destination_paths(self)
        fill_directory_tree(self.srcDir)
        create_archive(self.srcPath, self.archivePath)

    def tearDown(self):
        cleanup_temporary_directories(self)

    def test_can_extract_archive(self):
        extract_archive(self.archivePath, self.extractPath)

    def test_archive_represtantative_tree(self):
        # compare tree to archive
        extract_archive(self.archivePath, self.extractPath)
        dcmp = filecmp.dircmp(self.srcPath, self.extractPath)
        dcmp.report_full_closure()
        self.assertTrue(dcmp.common)
        self.assertFalse(dcmp.left_only)
        self.assertFalse(dcmp.right_only)
        self.assertFalse(dcmp.diff_files)
        self.assertFalse(dcmp.funny_files)
