from unittest import TestCase
#from nose.plugins.skip import SkipTest
from testfixtures import TempDirectory
from directory_fill_helpers import generate_filenames
from directory_fill_helpers import generate_file_contents
from directory_fill_helpers import write_files
from directory_fill_helpers import create_files
from directory_fill_helpers import generate_dirnames
from directory_fill_helpers import create_directories

class Test_directory_fill_helpers(TestCase):
    def setUp(self):
        self.testDir = TempDirectory()

    def tearDown(self):
        self.testDir.cleanup()

    def test_generate_filenames_one_file(self):
        fileNames = generate_filenames(1)
        self.assertTrue(fileNames == ['file0'])

    def test_generate_filenames_number_out_of_range(self):
        self.assertRaises(ValueError, generate_filenames, 0)
        self.assertRaises(ValueError, generate_filenames, 11)

    def test_generate_filenames_two_files(self):
        fileNames = generate_filenames(2)
        self.assertTrue(fileNames == ['file0', 'file1'])

    def test_genertate_file_contents_one_file(self):
        fileContents = generate_file_contents(1)
        self.assertTrue(fileContents == [''])

    def test_generate_file_contents_number_out_of_range(self):
        self.assertRaises(ValueError, generate_file_contents, 0)
        self.assertRaises(ValueError, generate_file_contents, 11)

    def test_generate_file_contents_two_files(self):
        fileContents = generate_file_contents(2)
        self.assertTrue(fileContents == ['', '1'])

    def test_write_test_files_one_file(self):
        fileNames = generate_filenames(1)
        fileContents = generate_file_contents(1)
        files = zip(fileNames, fileContents)
        write_files(self.testDir, files)
        self.testDir.check(*fileNames)
        
    def test_write_test_files_ten_files(self):
        fileNames = generate_filenames(10)
        fileContents = generate_file_contents(10)
        files = zip(fileNames, fileContents)
        write_files(self.testDir, files)
        self.testDir.check(*fileNames)

    def test_create_files_one_file(self):
        create_files(self.testDir, 1)
        self.testDir.check(*generate_filenames(1))

    def test_create_files_ten_files(self):
        create_files(self.testDir, 10)
        self.testDir.check(*generate_filenames(10))

    def test_generate_dirnames_one_dir(self):
        dirNames = generate_dirnames(1)
        self.assertTrue(dirNames == ['dir0'])

    def test_generate_dirnames_two_dirs(self):
        dirNames = generate_dirnames(2)
        self.assertTrue(dirNames == ['dir0', 'dir1'])

    def test_generate_dirnames_number_out_of_range(self):
        self.assertRaises(ValueError, generate_dirnames, 0)
        self.assertRaises(ValueError, generate_dirnames, 11)

    def test_create_directories_one_dir(self):
        create_directories(self.testDir, 1)
        self.testDir.check(*generate_dirnames(1))

    def test_create_directories_ten_dirs(self):
        create_directories(self.testDir, 10)
        self.testDir.check(*generate_dirnames(10))
