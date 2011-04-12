from unittest import TestCase
from bbpgsql.configuration import config
from bbpgsql.configuration.credentials import (
    get_aws_credentials,
    MissingCredentialsError,
    get_s3_connection,
    )
from mock import patch


class Test_AWSCredentials(TestCase):
    def setUp(self):
        self.config = config()
        self.config.set('Credentials', 'aws_access_key_id', 'some_access_key')
        self.config.set('Credentials', 'aws_secret_key_id', 'some_secret_key')

    def test_can_get_aws_credentials_from_config(self):
        access_key, secret_key = get_aws_credentials(self.config)
        self.assertEqual('some_access_key', access_key)
        self.assertEqual('some_secret_key', secret_key)


class Test_AWSCredentials_With_Missing_Config_Values(TestCase):
    def setUp(self):
        self.config = config()

    def test_raises_MissingCredentialsError_on_missing_access_key(self):

        def will_raise_MissingCredentialsError():
            get_aws_credentials(self.config)

        self.assertRaises(MissingCredentialsError,
            will_raise_MissingCredentialsError)

    def test_raises_MissingCredentialsError_on_missing_secret_key(self):
        self.config.set('Credentials', 'aws_access_key_id', 'some_access_key')

        def will_raise_MissingCredentialsError():
            get_aws_credentials(self.config)

        self.assertRaises(MissingCredentialsError,
            will_raise_MissingCredentialsError)


class Test_GetS3Connection_WithCredentials(TestCase):
    @patch('bbpgsql.configuration.credentials.connect_s3')
    def test_will_return_s3_connection(self, mock_connect_s3):
        get_s3_connection('access_key', 'secret_key')
        mock_connect_s3.assert_called_with('access_key', 'secret_key')
