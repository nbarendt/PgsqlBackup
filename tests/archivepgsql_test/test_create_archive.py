from unittest import TestCase
from testfixtures import TempDirectory
from nose.plugins.skip import SkipTest
import os
import tarfile
from bbpgsql.create_archive import create_archive


class Test_archive_create(TestCase):
    def setUp(self):
        self.create_valid_source_and_destination_paths()
        self.create_invalid_source_and_destination_paths()

    def tearDown(self):
        self.cleanup_temporary_directories()

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
            self.member_is_at_absolute_path(member)

    def test_archive_file_contains_no_up_references_above_root(self):
        raise(SkipTest)
        self.fail('Not implemented yet')

    def test_archive_represtantative_tree(self):
        raise(SkipTest)
        self.fill_directory_tree(self)
        create_archive(self.srcPath, self.archivePath)
        # compare tree to archive -- Hey! It needs the extract_archive function
        self.fail(msg='Extracted archive and original tree differ')

    def fill_directory_tree(self):
        print(self.srcDir.write('file0', ''))
        print(self.srcDir.write('file1', '1'))
        print(self.srcDir.makedir('dir0'))
        print(self.srcDir.write(('dir1', 'file0'), ''))
        print(self.srcDir.write(('dir1', 'file1'), '1'))
        print(self.srcDir.makedir(('dir1', 'dir0')))
        print(self.srcDir.write(('dir1', 'dir1', 'file0'), ''))
        print(self.srcDir.write(('dir1', 'dir1', 'file1'), '1'))

    def member_is_at_absolute_path(self, member):
        self.assertFalse(os.path.isabs(member.name))

    def create_valid_source_and_destination_paths(self):
        self.srcDir = TempDirectory()
        self.destDir = TempDirectory()
        self.srcPath = self.srcDir.path
        self.archiveName = 'archive.tar'
        self.archivePath = os.path.join(self.destDir.path, self.archiveName)

    def create_invalid_source_and_destination_paths(self):
        self.invalidDirParent = TempDirectory()
        self.invalidPath = os.path.join(self.invalidDirParent.path,
            'thisDirDoesNotExist')
        self.invalidSrcDir = self.invalidPath
        self.invalidArchivePath = os.path.join(self.invalidPath,
            self.archiveName)

    def cleanup_temporary_directories(self):
        self.srcDir.cleanup()
        self.destDir.cleanup()
        self.invalidDirParent.cleanup()
