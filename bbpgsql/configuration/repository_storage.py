from bbpgsql.repository_storage_memory import MemoryCommitStorage
from bbpgsql.repository_storage_filesystem import FilesystemCommitStorage
from bbpgsql.repository_storage_s3 import S3CommitStorage
from bbpgsql.configuration.credentials import (
    get_aws_credentials,
    get_s3_connection,
    )
from ConfigParser import NoOptionError


class MissingS3Configuration(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def create_memory_commit_store_from_config(config, section):
    return MemoryCommitStorage()


def create_filesystem_commit_store_from_config(config, section):
    storage_directory = config.get(section, 'path')
    return FilesystemCommitStorage(storage_directory)

SECTION_NAME = 'WAL storage'
BUCKET_KEY_NAME = 'bucket'
KEY_PREFIX_NAME = 'prefix'


def create_s3_commit_store_from_config(config, section):
    try:
        bucket_name = config.get(section, BUCKET_KEY_NAME)
    except NoOptionError:
        raise MissingS3Configuration('A "{0}" value must be provided in the' \
            ' "{1}" section when using the S3 driver.'.format(BUCKET_KEY_NAME,
            SECTION_NAME))

    try:
        key_prefix = config.get(section, KEY_PREFIX_NAME)
    except NoOptionError:
        raise MissingS3Configuration('A "{0}" value must be provided in the' \
            ' "{1}" section when using the S3 driver.'.format(KEY_PREFIX_NAME,
            SECTION_NAME))

    access_key, secret_key = get_aws_credentials(config)
    conn = get_s3_connection(access_key, secret_key)
    bucket = conn.create_bucket(bucket_name)
    return S3CommitStorage(bucket, key_prefix)


def get_WAL_storage_from_config(config):
    STORAGE_DRIVERS = {
        'memory': create_memory_commit_store_from_config,
        'filesystem': create_filesystem_commit_store_from_config,
        's3': create_s3_commit_store_from_config,
    }

    storage_driver = config.get(SECTION_NAME, 'driver')
    storage_driver_factory = STORAGE_DRIVERS[storage_driver]
    return storage_driver_factory(config, SECTION_NAME)
