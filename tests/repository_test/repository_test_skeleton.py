from unittest import TestCase
from testfixtures import TempDirectory
from bbpgsql.repository import BBRepository
from bbpgsql.repository import DuplicateTagError


class Skeleton_Repository_Operations_With_SpecificCommitStorage(TestCase):
    __test__ = False  # to prevent nose from running this skeleton

    def setUp(self):
        raise Exception('This is a skeleton for test - you need to provide'
                        ' your own setUp() and tearDown()')

    def setup_tempdir(self):
        # call this from your setUp
        self.tempdir = TempDirectory()
        self.file1 = self.tempdir.write('file1', 'some contents')
        self.file2 = self.tempdir.write('file2', 'some other contents')

    def teardown_tempdir(self):
        # call this from your tearDown
        self.tempdir.cleanup()

    def setup_repository(self):
        # call this from your setUp after creating your store
        self.repo = BBRepository(self.store)

    def commit_file1(self, tag, message=None):
        self.repo.create_commit_from_filename(tag, self.file1, message)

    def commit_file2(self, tag, message=None):
        self.repo.create_commit_from_filename(tag, self.file2, message)

    def test_can_commit_files_to_repository(self):
        self.commit_file1('some_tag')

    def test_commit_tag_characters_are_limited(self):
        def will_raise_Exception():
            self.commit_file1('illegal tag with spaces')
        self.assertRaises(Exception, will_raise_Exception)

    def test_commit_tag_must_be_non_empty(self):
        def will_raise_Exception():
            self.commit_file1('')
        self.assertRaises(Exception, will_raise_Exception)

    def test_repo_is_empty_to_start(self):
        self.assertEqual([], [c for c in self.repo])

    def test_can_commit_files_and_list_commits(self):
        self.commit_file1('some_tag')
        self.assertEqual(['some_tag'], [c.tag for c in self.repo])

    def test_can_commit_and_retrieve_contents(self):
        self.commit_file1('some_tag')
        commit = self.repo['some_tag']
        restore_file = self.tempdir.getpath('file3')
        commit.get_contents_to_filename(restore_file)
        self.assertEqual('some contents', open(restore_file, 'rb').read())
    
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

