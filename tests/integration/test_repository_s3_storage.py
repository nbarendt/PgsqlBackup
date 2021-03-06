from bbpgsql.repository_storage_s3 import S3CommitStorage
from tests.integration.s3_helpers import setup_s3_and_bucket
from uuid import uuid4
from tests.repository_test.repository_test_skeleton import (
    Skeleton_Repository_Operations_With_SpecificCommitStorage
    )


class Skeleton_Repository_Operations_With_S3CommitStorage(
    Skeleton_Repository_Operations_With_SpecificCommitStorage):

    def setUp(self):
        self.setup_tempdir()
        self.setup_bucket()
        self.store = self.create_storage()  # tests need to provide
        self.setup_repository()

    def setup_bucket(self):
        self.bucket_name = '.'.join(['test', uuid4().hex])
        self.temps3 = setup_s3_and_bucket(self.bucket_name)
        self.bucket = self.temps3.bucket

    def tearDown(self):
        self.temps3.cleanup()
        self.teardown_tempdir()

    def get_lone_key(self):
        keys = [k for k in self.bucket.list(prefix=self.bucket_prefix)]
        self.assertEqual(1, len(keys))
        return self.bucket.get_key(keys[0])

    def test_key_in_s3_has_required_metadata(self):
        self.commit_filename1('a')
        key = self.get_lone_key()
        self.assertIsNotNone(key.etag)
        self.assertEqual(key.content_encoding, 'gzip')
        self.assertEqual(key.content_type, 'application/octet-stream')

    def get_expected_size_from_contents(self, file_contents):
        return sum(k.size for k in self.bucket.list(prefix=self.bucket_prefix))


class Test_Repository_Operations_with_S3CommitStorage(
    Skeleton_Repository_Operations_With_S3CommitStorage):
    __test__ = True

    def create_storage(self):
        self.bucket_prefix = ''
        return S3CommitStorage(self.bucket)


class Test_Repository_Operations_with_S3CommitStorage_with_Bucket_Prefix(
    Skeleton_Repository_Operations_With_S3CommitStorage):
    __test__ = True

    def create_storage(self):
        self.bucket_prefix = 'some_test_prefix/'
        self.bucket.new_key('some_random_key').set_contents_from_string(
            'some_random_string')
        return S3CommitStorage(self.bucket, self.bucket_prefix)
