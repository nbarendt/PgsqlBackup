from unittest import TestCase
from nose.plugins.skip import SkipTest
import os
import tarfile
import filecmp
from bbpgsql.create_archive import create_archive
from bbpgsql.create_archive import generate_exclude
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

    def test_create_archive_excludes_directory(self):
        fill_directory_tree(self.srcDir)
        self.excludeList = ['./dir2']
        create_archive(self.srcPath, self.archivePath, self.excludeList)
        tf = tarfile.open(self.archivePath, mode='r')

        def getExcludedMember(name):
            tarinfo = tf.getmember(name)
            if tarinfo:
                pass

        self.assertRaises(KeyError, getExcludedMember, './dir2')

    def test_create_archive_excludes_two_directories(self):
        fill_directory_tree(self.srcDir)
        self.excludeList = ['./dir2', './dir0']
        create_archive(self.srcPath, self.archivePath, self.excludeList)
        tf = tarfile.open(self.archivePath, mode='r')

        def getExcludedMember(name):
            tarinfo = tf.getmember(name)
            if tarinfo:
                pass

        for root, dirs, files in os.walk(self.srcPath):
            relativeRoot = os.path.relpath(root, self.srcPath)
            dirs_to_remove = []
            if relativeRoot != '.':
                relativeRoot = ''.join(['./', relativeRoot])
            for file in files:
                relfile = os.path.join(relativeRoot, file)
                if relfile in self.excludeList:
                    print('Checking file is excluded:', root, file, relfile)
                    self.assertRaises(KeyError,
                        getExcludedMember, relfile)
                else:
                    print('Checking file is included:', root, file, relfile)
                    self.assertNotEqual(None,
                        tf.getmember(relfile))
            for dir in dirs:
                reldir = os.path.join(relativeRoot, dir)
                if reldir in self.excludeList:
                    print('Checking dir is excluded:', root, dir, reldir)
                    self.assertRaises(KeyError,
                        getExcludedMember, reldir)
                    subTreePath = os.path.join(root, dir)
                    print('checking subtree', subTreePath)
                    for root2, dirs2, files2 in os.walk(subTreePath):
                        print('element subtree', root2, dirs2, files2)
                        relativeRoot2 = os.path.relpath(root2, self.srcPath)
                        if relativeRoot2 != '.':
                            relativeRoot2 = ''.join(['./', relativeRoot2])
                        for file2 in files2:
                            relfile2 = os.path.join(relativeRoot2, file2)
                            print('Checking file is excluded:',
                                root2, file2, relfile2)
                            self.assertRaises(KeyError,
                                getExcludedMember, relfile2)
                        for dir2 in dirs2:
                            reldir2 = os.path.join(relativeRoot2, dir2)
                            print('Checking dir is excluded:',
                                root2, dir2, reldir2)
                            self.assertRaises(KeyError,
                                getExcludedMember, reldir2)
                    dirs_to_remove.append(dir)
                else:
                    print('Checking dir is included:', root, dir, reldir)
                    self.assertNotEqual(None,
                        tf.getmember(reldir))
             
            for d in dirs_to_remove:
              dirs.remove(d)
 
class Test_generate_exclude(TestCase):
    def setUp(self):
        self.excludeList = ['exclude_this', 'exclude_this_too']
        self.keepList = ['keep_this', 'keep_this_too']
        self.excluded = tarfile.TarInfo(name=self.excludeList[0])
        self.excluded_too = tarfile.TarInfo(name=self.excludeList[1])
        self.kept = tarfile.TarInfo(name=self.keepList[0])
        self.kept_too = tarfile.TarInfo(name=self.keepList[1])
        self.function = generate_exclude(self.excludeList)

    def tearDown(self):
        pass

    def test_generate_exclude_returns_function(self):
        self.assertTrue(hasattr(self.function, '__call__'))

    def test_generate_exclude_function_takes_one_argument(self):
        self.retval = self.function(self.kept)

    def test_generated_function_returns_input_kept_object(self):
        self.retval = self.function(self.kept)
        self.assertEqual(self.retval, self.kept)

    def test_generated_function_returns_input_kept_too_object(self):
        self.retval = self.function(self.kept_too)
        self.assertEqual(self.retval, self.kept_too)

    def test_generated_function_returns_none_for_excluded_object(self):
        self.retval = self.function(self.excluded)
        self.assertEqual(self.retval, None)

    def test_generated_function_returns_none_for_excluded_too_object(self):
        self.retval = self.function(self.excluded_too)
        self.assertEqual(self.retval, None)
