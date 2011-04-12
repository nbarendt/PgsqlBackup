from ConfigParser import SafeConfigParser
from boto import connect_s3

TEST_AWS_CREDENTIAL_FILE = 'aws_test.ini'

def get_test_aws_credentials():
    configFile = SafeConfigParser()
    configFile.read(TEST_AWS_CREDENTIAL_FILE)
    aws_access_key = configFile.get('aws', 'aws_access_key')
    aws_secret_key = configFile.get('aws', 'aws_secret_key')
    return aws_access_key, aws_secret_key

def get_s3_connection(access_key, secret_key):
    return connect_s3(access_key, secret_key)

class S3TestFixture(object):
    def __init__(self, access_key, secret_key, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name

    @property
    def connection(self):
        return get_s3_connection(self.access_key, self.secret_key)

    @property
    def bucket(self):
        return self.connection.create_bucket(self.bucket_name)

    def cleanup(self):
        for key in self.bucket:
            key.delete()
        self.bucket.delete()

def setup_s3_and_bucket(bucket_name):
    access_key, secret_key = get_test_aws_credentials()
    return S3TestFixture(access_key, secret_key, bucket_name)
    
    


