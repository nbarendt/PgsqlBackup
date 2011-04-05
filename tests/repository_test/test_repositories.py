from unittest import TestCase
from testfixtures import TempDirectory
from bbpgsql.repository import DuplicateTagError
from bbpgsql.repository import BBRepository
from bbpgsql.repository_storage_test import MemoryCommitStorage
from bbpgsql.repository_storage_test import FilesystemCommitStorage

class Test_DuplicateTagError(TestCase):
    def test_str_output(self):
        expected = 'DuplicateTagError: the tag "badtag" already' \
                    ' exists in the repository'
        self.assertEqual(expected, str(DuplicateTagError('badtag')))

class Test_Repository_Operations_With_MemoryCommitStorage(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.store = MemoryCommitStorage()
        self.repo = BBRepository(self.store)
        self.file1 = self.tempdir.write('file1', 'some contents')
        self.file2 = self.tempdir.write('file2', 'some other contents')

    def tearDown(self):
        self.tempdir.cleanup()

    def commit_file1(self, tag, message=None):
        self.repo.create_commit_from_filename(tag, self.file1, message)

    def commit_file2(self, tag, message=None):
        self.repo.create_commit_from_filename(tag, self.file2, message)

    def test_can_commit_files_to_repository(self):
        self.commit_file1('some_tag')

    def test_commit_tag_characters_limited(self):
        def will_raise_Exception():
            self.commit_file1('illegal tag with spaces')
        self.assertRaises(Exception, will_raise_Exception)

    def test_repo_is_empty_to_start(self):
        self.assertEqual([], [c for c in self.repo])

    def test_can_commit_files_and_list_commits(self):
        self.commit_file1('some_tag')
        self.assertEqual(['some_tag'], [c.tag for c in self.repo])

    def test_can_commit_and_retrieve_contents(self):
        self.commit_file1('some_tag')
        commit = self.repo['some_tag']
        commit.get_contents_to_filename(self.file2)
        self.assertEqual('some contents', open(self.file2, 'rb').read())
    
    def test_tags_are_unique(self):
        self.commit_file1('some_tag')

        def will_raise_DuplicateTagError():
            self.repo.create_commit_from_filename('some_tag', self.file1)
        self.assertRaises(DuplicateTagError, will_raise_DuplicateTagError)

    def test_can_get_commit_before_a_given_commit(self):
        self.commit_file1('a')
        self.commit_file1('b')
        commit_b = self.repo['b']
        self.assertEqual('a', self.repo.get_commit_before(commit_b).tag)

    def test_commit_before_first_raises_ValueError(self):
        self.commit_file1('a')

        def will_raise_ValueError():
            self.repo.get_commit_before(self.repo['a'])
        self.assertRaises(ValueError, will_raise_ValueError)

    def test_commits_are_sorted(self):
        self.commit_file1('c')
        self.commit_file1('a')
        self.commit_file1('b')
        self.assertEqual(['a', 'b', 'c'], [c.tag for c in self.repo])

    def test_can_delete_commits_before_a_specified_commit(self):
        self.commit_file1('a')
        self.commit_file1('b')
        self.commit_file1('c')
        self.repo.delete_commits_before(self.repo['c'])
        self.assertEqual(['c'], [c.tag for c in self.repo])

    def test_can_store_and_retrieve_message_with_commit(self):
        message = 'some_extra_data'
        self.commit_file1('a', message)
        commit = self.repo['a']
        self.assertEqual(message, commit.message)

    def test_message_characters_limited_to_alphanumeric_and_underscore(self):

        def will_raise_Exception():
            self.commit_file1('a', 'some illegal message')
        self.assertRaises(Exception, will_raise_Exception)


class Test_Basic_Rpository_Operations_On_FilesystemRepository(
        Test_Repository_Operations_With_MemoryCommitStorage):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.repo_path = self.tempdir.makedir('repo')
        self.store = FilesystemCommitStorage(self.repo_path)
        self.repo = BBRepository(self.store)
        self.file1 = self.tempdir.write('self.file1', 'some contents')
        self.file2 = self.tempdir.write('file2', 'some other contents')

