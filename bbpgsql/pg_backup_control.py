from subprocess import check_output
from re import match

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
        return '{0}.{1}'.format(match_results.group(1), match_results.group(2))
    else:
        raise Exception('Unable to determine psql version')

def pg_start_backup(label):
    cmd_prefix = "SELECT pg_xlogfile_name(pg_start_backup('"
    cmd_suffix = "', true));"
    sql_cmd = ''.join([cmd_prefix, label, cmd_suffix])
    CMD = []
    CMD.append('psql') # what the's path?
    CMD.append('postgres') # need the right database
    CMD.append('-t') # return tuple only, no headers
    CMD.append('-c') # execute the following command
    CMD.append(sql_cmd)
    return wal_name_cleanup(check_output(CMD))

def wal_name_cleanup(input):
    return input.strip()

def pg_stop_backup():
    sql_cmd = "SELECT pg_xlogfile_name(pg_stop_backup())"
    CMD = []
    CMD.append('psql') # what the's path?
    CMD.append('postgres') # need the right database
    CMD.append('-t') # return tuple only, no headers
    CMD.append('-c') # execute the following command
    CMD.append(sql_cmd)
    return wal_name_cleanup(check_output(CMD))
