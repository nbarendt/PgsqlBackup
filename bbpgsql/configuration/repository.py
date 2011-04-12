from bbpgsql.repository import BBRepository
from bbpgsql.configuration.repository_storage import (
    get_WAL_storage_from_config
)


def get_WAL_repository(config):
    commit_storage = get_WAL_storage_from_config(config)
    return BBRepository(commit_storage)
