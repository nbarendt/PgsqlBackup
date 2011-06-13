from uuid import uuid4
from tests.storagestats_tests.test_cmdline import (
    Test_storestats_with_real_repos
)
from tests.integration.s3_helpers import setup_s3_and_bucket
from tests.integration.s3_helpers import generate_s3_config


class Test_storagestats_with_s3(Test_storestats_with_real_repos):
    def setup_s3(self):
        self.bucket_name = '.'.join(['test', uuid4().hex])
        self.temps3 = setup_s3_and_bucket(self.bucket_name)

    def setup_config(self):
        self.setup_s3()
        return generate_s3_config(
                self.temps3.access_key,
                self.temps3.secret_key,
                self.bucket_name,
                self.tempdir.path)

    def teardown_customize(self):
        self.temps3.cleanup()
        self.tempdir.cleanup()
