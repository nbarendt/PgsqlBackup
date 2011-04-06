from unittest import TestCase
from bbpgsql.repository import DuplicateTagError
from bbpgsql.repository_storage_test import MemoryCommitStorage
from bbpgsql.repository_storage_test import FilesystemCommitStorage
from bbpgsql.repository_storage_s3 import S3CommitStorage
from ConfigParser import SafeConfigParser
from boto import connect_s3
from uuid import uuid4
from tests.repository_test.repository_test_skeleton import (
    Skeleton_Repository_Operations_With_SpecificCommitStorage
    )


class Test_DuplicateTagError(TestCase):
    def test_str_output(self):
        expected = 'DuplicateTagError: the tag "badtag" already' \
                    ' exists in the repository'
        self.assertEqual(expected, str(DuplicateTagError('badtag')))

class Test_Repository_Operations_With_MemoryCommitStorage(
    Skeleton_Repository_Operations_With_SpecificCommitStorage):
    __test__ = True

    def setUp(self):
        self.setup_tempdir()
        self.store = MemoryCommitStorage()
        self.setup_repository()

    def tearDown(self):
        self.teardown_tempdir()

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


class Test_Repository_Operations_With_FileSystemCommitStore(
    Skeleton_Repository_Operations_With_SpecificCommitStorage):
    __test__ = True

    def setUp(self):
        self.setup_tempdir()
        self.repo_path = self.tempdir.makedir('repo')
        self.store = FilesystemCommitStorage(self.repo_path)
        self.setup_repository()

    def tearDown(self):
        self.teardown_tempdir()

class Test_Repository_Operations_With_S3CommitStorage(
    Skeleton_Repository_Operations_With_SpecificCommitStorage):
    __test__ = True

    def setUp(self):
        self.setup_tempdir()
        configFile = SafeConfigParser()
        configFile.read('aws_test.ini')
        aws_access_key = configFile.get('aws', 'aws_access_key')
        aws_secret_key = configFile.get('aws', 'aws_secret_key')
        self.s3_connection = connect_s3(aws_access_key, aws_secret_key)
        self.bucket_name = '.'.join(['test', uuid4().hex])
        self.bucket = self.s3_connection.create_bucket(self.bucket_name)
        self.store = S3CommitStorage(self.bucket)
        self.repo_path = self.tempdir.makedir('repo')
        self.setup_repository()

    def tearDown(self):
        for key in self.bucket:
            key.delete()
        self.bucket.delete()
        self.teardown_tempdir()
