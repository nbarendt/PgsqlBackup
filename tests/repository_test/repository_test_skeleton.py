from unittest import TestCase
from testfixtures import TempDirectory
from bbpgsql.repository import BBRepository
from bbpgsql.repository import DuplicateTagError
from datetime import datetime


class Skeleton_Repository_Operations_With_SpecificCommitStorage(TestCase):
    __test__ = False  # to prevent nose from running this skeleton

    def setUp(self):
        raise Exception('This is a skeleton for test - you need to provide'
                        ' your own setUp() and tearDown()')

    def setup_tempdir(self):
        # call this from your setUp
        self.tempdir = TempDirectory()
        self.file1_contents = 'some contents'
        self.file2_contents = 'some other contents'
        self.filename1 = self.tempdir.write('file1', self.file1_contents)
        self.filename2 = self.tempdir.write('file2', self.file2_contents)

    def teardown_tempdir(self):
        # call this from your tearDown
        self.tempdir.cleanup()

    def setup_repository(self):
        # call this from your setUp after creating your store
        self.repo = BBRepository(self.store)

    def commit_filename1(self, tag, message=None):
        self.repo.create_commit_from_filename(tag, self.filename1, message)

    def commit_filename2(self, tag, message=None):
        self.repo.create_commit_from_filename(tag, self.filename2, message)

    def test_can_commit_filenames_to_repository(self):
        self.commit_filename1('some-tag')

    def test_commit_tag_characters_are_limited(self):
        def will_raise_Exception():
            self.commit_filename1('illegal tag with spaces')
        self.assertRaises(Exception, will_raise_Exception)

    def test_commit_tag_must_be_non_empty(self):
        def will_raise_Exception():
            self.commit_filename1('')
        self.assertRaises(Exception, will_raise_Exception)

    def test_repo_is_empty_to_start(self):
        self.assertEqual([], [c for c in self.repo])

    def test_can_commit_files_and_list_commits(self):
        self.commit_filename1('some-tag')
        self.assertEqual(['some-tag'], [c.tag for c in self.repo])

    def test_can_commit_and_retrieve_contents(self):
        self.commit_filename1('some-tag')
        commit = self.repo['some-tag']
        restore_file = self.tempdir.getpath('file3')
        commit.get_contents_to_filename(restore_file)
        self.assertEqual(self.file1_contents, open(restore_file, 'rb').read())

    def test_tags_are_unique(self):
        self.commit_filename1('some-tag')

        def will_raise_DuplicateTagError():
            self.repo.create_commit_from_filename('some-tag', self.filename2)
        self.assertRaises(DuplicateTagError, will_raise_DuplicateTagError)

    def test_duplicate_tag_with_identical_contents_okay(self):
        self.commit_filename1('some-tag')
        self.commit_filename1('some-tag')
        commit = self.repo['some-tag']
        restore_file = self.tempdir.getpath('file3')
        commit.get_contents_to_filename(restore_file)
        self.assertEqual(self.file1_contents, open(restore_file, 'rb').read())

    def test_can_get_commit_before_a_given_commit(self):
        self.commit_filename1('a')
        self.commit_filename1('b')
        commit_b = self.repo['b']
        self.assertEqual('a', self.repo.get_commit_before(commit_b).tag)

    def test_commit_before_first_raises_ValueError(self):
        self.commit_filename1('a')

        def will_raise_ValueError():
            self.repo.get_commit_before(self.repo['a'])
        self.assertRaises(ValueError, will_raise_ValueError)

    def test_commits_are_sorted(self):
        self.commit_filename1('c')
        self.commit_filename1('a')
        self.commit_filename1('b')
        self.assertEqual(['a', 'b', 'c'], [c.tag for c in self.repo])

    def test_can_delete_commits_before_a_specified_commit(self):
        self.commit_filename1('a')
        self.commit_filename1('b')
        self.commit_filename1('c')
        self.repo.delete_commits_before(self.repo['c'])
        self.assertEqual(['c'], [c.tag for c in self.repo])

    def test_can_store_and_retrieve_message_with_commit(self):
        message = 'some-extra-data'
        self.commit_filename1('a', message)
        commit = self.repo['a']
        self.assertEqual(message, commit.message)

    def test_message_characters_limited_to_alphanumeric_and_underscore(self):

        def will_raise_Exception():
            self.commit_filename1('a', 'some illegal message')
        self.assertRaises(Exception, will_raise_Exception)

    def test_UTC_iso_datetime_is_a_valid_tag(self):
        self.commit_filename1(datetime.utcnow().isoformat())

    def test_UTC_iso_datetime_is_a_valid_message(self):
        self.commit_filename1('a', datetime.utcnow().isoformat())
        self.commit_filename1(datetime.utcnow().isoformat())
