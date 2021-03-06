from unittest import TestCase
from testfixtures import TempDirectory
from bbpgsql.configuration import config
from bbpgsql.configuration.repository_storage import (
    get_repository_storage_from_config,
    MissingS3Configuration,
    )
from bbpgsql.repository_storage_memory import MemoryCommitStorage
from bbpgsql.repository_storage_filesystem import FilesystemCommitStorage
from bbpgsql.repository_storage_s3 import S3CommitStorage
from mock import patch


class Test_Storage_Configurations(TestCase):

    def test_default_WAL_storage_is_S3(self):
        self.assertEqual('s3', config().get('WAL', 'driver'))


class Test_StorageFactory_From_Configuration(TestCase):

    def setUp(self):
        self.config = config()

    def configure_driver(self, driver_type):
        self.config.set('WAL', 'driver', driver_type)

    @patch('bbpgsql.configuration.repository_storage'
                '.create_memory_commit_store_from_config')
    def test_memory_driver_factory_called(self, factory_mock):
        self.configure_driver('memory')
        get_repository_storage_from_config(self.config, 'WAL')
        factory_mock.assert_called_with(self.config, 'WAL')

    @patch('bbpgsql.configuration.repository_storage'
                '.create_filesystem_commit_store_from_config')
    def test_filesystem_driver_factory_called(self, factory_mock):
        self.configure_driver('filesystem')
        get_repository_storage_from_config(self.config, 'WAL')
        factory_mock.assert_called_with(self.config, 'WAL')

    @patch('bbpgsql.configuration.repository_storage'
                '.create_s3_commit_store_from_config')
    def test_s3_driver_factory_called(self, factory_mock):
        self.configure_driver('s3')
        get_repository_storage_from_config(self.config, 'WAL')
        factory_mock.assert_called_with(self.config, 'WAL')


class Test_MemoryCommit_Storage(TestCase):
    def setUp(self):
        self.config = config()
        self.config.set('WAL', 'driver', 'memory')

    def test_will_build_storage_from_config(self):
        self.assertEqual(MemoryCommitStorage,
            type(get_repository_storage_from_config(self.config, 'WAL')))


class Test_FilesystemCommitStorage(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.commit_storage_path = self.tempdir.makedir('commit_storage')
        self.config = config()
        self.config.set('WAL', 'driver', 'filesystem')
        self.config.set('WAL', 'path', self.commit_storage_path)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_will_build_storage_from_config(self):
        self.assertEqual(FilesystemCommitStorage,
            type(get_repository_storage_from_config(self.config, 'WAL')))


class Test_S3CommitStorage(TestCase):
    def setUp(self):
        self.config = config()
        self.config.set('WAL', 'driver', 's3')
        self.config.set('Credentials', 'aws_access_key_id', 'some_access_key')
        self.config.set('Credentials', 'aws_secret_key_id', 'some_secret_key')

    def test_will_raise_MissingS3Configuration_without_bucket(self):

        def will_raise_MissingS3Configuration():
            get_repository_storage_from_config(self.config, 'WAL')
        self.assertRaises(MissingS3Configuration,
            will_raise_MissingS3Configuration)

    def test_will_raise_MissingS3Configuration_without_prefix(self):
        self.config.set('WAL', 'bucket', 'somebucket')

        def will_raise_MissingS3Configuration():
            get_repository_storage_from_config(self.config, 'WAL')
        self.assertRaises(MissingS3Configuration,
            will_raise_MissingS3Configuration)

    @patch('bbpgsql.configuration.repository_storage.get_s3_connection')
    def test_will_build_storage_from_config(self, mock_get_s3_connection):
        self.config.set('General', 'bucket', 'somebucket')
        self.assertEqual(S3CommitStorage,
            type(get_repository_storage_from_config(self.config, 'WAL')))
        mock_get_s3_connection.assert_called_with('some_access_key',
            'some_secret_key')
