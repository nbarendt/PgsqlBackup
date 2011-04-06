from bbpgsql.repository_storage_s3 import S3CommitStorage
from ConfigParser import SafeConfigParser
from boto import connect_s3
from uuid import uuid4
from tests.repository_test.repository_test_skeleton import (
    Skeleton_Repository_Operations_With_SpecificCommitStorage
    )


class Skeleton_Repository_Operations_With_S3CommitStorage(
    Skeleton_Repository_Operations_With_SpecificCommitStorage):

    def setUp(self):
        self.setup_tempdir()
        self.setup_bucket()
        self.store = self.create_storage() # tests need to provide
        self.setup_repository()

    def setup_bucket(self):
        configFile = SafeConfigParser()
        configFile.read('aws_test.ini')
        aws_access_key = configFile.get('aws', 'aws_access_key')
        aws_secret_key = configFile.get('aws', 'aws_secret_key')
        self.s3_connection = connect_s3(aws_access_key, aws_secret_key)
        self.bucket_name = '.'.join(['test', uuid4().hex])
        self.bucket = self.s3_connection.create_bucket(self.bucket_name)

    def tearDown(self):
        self.teardown_bucket()
        self.teardown_tempdir()

    def teardown_bucket(self):
        for key in self.bucket:
            key.delete()
        self.bucket.delete()


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
