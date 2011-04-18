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


class Test_Repository_Operations_with_S3CommitStorage(
    Skeleton_Repository_Operations_With_S3CommitStorage):
    __test__ = True

    def create_storage(self):
        return S3CommitStorage(self.bucket)


class Test_Repository_Operations_with_S3CommitStorage_with_Bucket_Prefix(
    Skeleton_Repository_Operations_With_S3CommitStorage):
    __test__ = True

    def create_storage(self):
        return S3CommitStorage(self.bucket, 'some_test_prefix/')
