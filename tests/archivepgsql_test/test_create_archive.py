from unittest import TestCase
from nose.plugins.skip import SkipTest
import os
import tarfile
import filecmp
from bbpgsql.create_archive import create_archive
from bbpgsql.extract_archive import extract_archive
from tar_archive_helpers import fill_directory_tree
from tar_archive_helpers import create_valid_source_and_destination_paths
from tar_archive_helpers import create_invalid_source_and_destination_paths
from tar_archive_helpers import cleanup_temporary_directories
from tar_archive_helpers import member_is_at_relative_path


class Test_archive_create(TestCase):
    def setUp(self):
        create_valid_source_and_destination_paths(self)
        create_invalid_source_and_destination_paths(self)

    def tearDown(self):
        cleanup_temporary_directories(self)

    def test_can_create_archive_file(self):
        create_archive(self.srcPath, self.archivePath)
        self.fh = open(self.archivePath)

    def test_archive_is_nonempty(self):
        create_archive(self.srcPath, self.archivePath)
        self.assertTrue(os.stat(self.archivePath).st_size > 0,
            msg='Created archive size was 0 or less')

    def test_archive_is_a_tar_archive(self):
        create_archive(self.srcPath, self.archivePath)
        self.assertTrue(tarfile.is_tarfile(self.archivePath),
            msg='Created archive not a valid tar file')

    def test_archive_fails_when_source_does_not_exist(self):

        def invalidPath():
            create_archive(self.invalidSrcDir, self.archivePath)

        self.assertRaises(Exception, invalidPath)

    def test_archive_fails_when_destination_does_not_exist(self):

        def invalidPath():
            create_archive(self.srcPath, self.invalidArchivePath)

        self.assertRaises(Exception, invalidPath)

    def test_archive_file_contains_no_absolute_paths(self):
        create_archive(self.srcPath, self.archivePath)
        self.tf = tarfile.open(name=self.archivePath, mode='r')
        for member in self.tf:
            self.assertTrue(member_is_at_relative_path(member))

    def test_archive_file_contains_no_up_references_above_root(self):
        raise(SkipTest)
        self.fail('Not implemented yet')

    def test_archive_represtantative_tree(self):
        fill_directory_tree(self.srcDir)
        create_archive(self.srcPath, self.archivePath)
        # compare tree to archive
        extract_archive(self.archivePath, self.extractPath)
        dcmp = filecmp.dircmp(self.srcPath, self.extractPath)
        dcmp.report_full_closure()
        self.assertTrue(dcmp.common)
        self.assertFalse(dcmp.left_only)
        self.assertFalse(dcmp.right_only)
        self.assertFalse(dcmp.diff_files)
        self.assertFalse(dcmp.funny_files)
