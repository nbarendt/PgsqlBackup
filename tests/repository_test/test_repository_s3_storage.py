from bbpgsql.repository_storage_s3 import S3CommitStorage
from ConfigParser import SafeConfigParser
from boto import connect_s3
from uuid import uuid4
from tests.repository_test.repository_test_skeleton import (
    Skeleton_Repository_Operations_With_SpecificCommitStorage
    )


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
