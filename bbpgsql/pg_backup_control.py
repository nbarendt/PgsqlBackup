from subprocess import check_output
from re import match


PGSQL_START_BACKUP_SQL_COMMAND_STRING = {
    '8.2': "SELECT pg_xlogfile_name(pg_start_backup('{0}'));",
    '8.3': "SELECT pg_xlogfile_name(pg_start_backup('{0}'));",
    '8.4': "SELECT pg_xlogfile_name(pg_start_backup('{0}', true));",
    '9.0': "SELECT pg_xlogfile_name(pg_start_backup('{0}', true));",
}

PGSQL_SUPPORTED_VERSIONS = PGSQL_START_BACKUP_SQL_COMMAND_STRING.keys()


class UnsupportedPostgresVersionError(Exception):
    def __init__(self, version):
        self.msg = 'Unsupported Version Of Postgresql: {0}'.format(version)

    def __str__(self):
        return self.msg


def get_pg_version_output():
    CMD = []
    CMD.append('psql')
    CMD.append('--version')
    return check_output(CMD).strip()


def pg_get_version():
    version_string = get_pg_version_output().strip().split('\n')[0]
    version_regex = r'^psql\s\(PostgreSQL\)\s(\d+)\.(\d+)\.(\d+)$'
    match_results = match(version_regex, version_string)
    if match_results:
        version = '{0}.{1}'.format(match_results.group(1),
            match_results.group(2))
        if version not in PGSQL_SUPPORTED_VERSIONS:
            raise UnsupportedPostgresVersionError(version)
        return version
    else:
        raise Exception('Unable to determine psql version')


def pg_start_backup(label):
    pg_version = pg_get_version()
    sql_cmd = PGSQL_START_BACKUP_SQL_COMMAND_STRING[pg_version].format(label)

    CMD = []
    CMD.append('psql')  # what the's path?
    CMD.append('postgres')  # need the right database
    CMD.append('-t')  # return tuple only, no headers
    CMD.append('-c')  # execute the following command
    CMD.append(sql_cmd)
    return wal_name_cleanup(check_output(CMD))


def wal_name_cleanup(input):
    return input.strip()


def pg_stop_backup():
    sql_cmd = "SELECT pg_xlogfile_name(pg_stop_backup())"
    CMD = []
    CMD.append('psql')  # what the's path?
    CMD.append('postgres')  # need the right database
    CMD.append('-t')  # return tuple only, no headers
    CMD.append('-c')  # execute the following command
    CMD.append(sql_cmd)
    return wal_name_cleanup(check_output(CMD))
