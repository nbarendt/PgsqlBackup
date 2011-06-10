from uuid import uuid4
from tests.integration.s3_helpers import setup_s3_and_bucket
from tests.cmdline_test_skeleton import Cmdline_test_skeleton

class S3_Integration_Test_Skeleton(Cmdline_test_skeleton):
    exe_script = 'fill this in with your command'


    def setup_customize(self):
        pass

    def setup_s3(self):
        self.bucket_name = '.'.join(['test', uuid4().hex])
        self.prefix = 'wals/'
        self.temps3 = setup_s3_and_bucket(self.bucket_name)

    def setup_config(self):
        self.setup_s3()
        config_dict = {
            'General': {
                'pgsql_data_directory': self.tempdir.path,
                'bucket': self.bucket_name,
            },
            'Credentials': {
                'aws_access_key_id': self.temps3.access_key,
                'aws_secret_key_id': self.temps3.secret_key,
            },
        }
        return config_dict

    def teardown_customize(self):
        self.temps3.cleanup()
        self.tempdir.cleanup()
