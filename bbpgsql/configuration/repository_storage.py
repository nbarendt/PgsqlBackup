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


def create_s3_commit_store_from_config(config, repository_name):
    SECTION_NAME = 'General'
    BUCKET_KEY_NAME = 'bucket'
    KEY_PREFIX_NAME = 'prefix'
    REPOSITORY_TO_KEY_PREFIX_MAP = {
        'WAL': 'wals/',
        'Snapshot': 'snapshots/',
    }

    try:
        bucket_name = config.get(SECTION_NAME, BUCKET_KEY_NAME)
    except NoOptionError:
        raise MissingS3Configuration('A "{0}" value must be provided in the'
            ' "{1}" section when using the S3 driver.'.format(BUCKET_KEY_NAME,
            SECTION_NAME))

    common_prefix = ''
    if config.has_option(SECTION_NAME, KEY_PREFIX_NAME):
        common_prefix = config.get(SECTION_NAME, KEY_PREFIX_NAME)

    key_prefix = ''.join([common_prefix,
        REPOSITORY_TO_KEY_PREFIX_MAP[repository_name]])

    access_key, secret_key = get_aws_credentials(config)
    conn = get_s3_connection(access_key, secret_key)
    bucket = conn.create_bucket(bucket_name)
    return S3CommitStorage(bucket, key_prefix)


def get_repository_storage_from_config(config, repository_type):
    STORAGE_DRIVERS = {
        'memory': create_memory_commit_store_from_config,
        'filesystem': create_filesystem_commit_store_from_config,
        's3': create_s3_commit_store_from_config,
    }

    storage_driver = config.get(repository_type, 'driver')
    storage_driver_factory = STORAGE_DRIVERS[storage_driver]
    return storage_driver_factory(config, repository_type)
