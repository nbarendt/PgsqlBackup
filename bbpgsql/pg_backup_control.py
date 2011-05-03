from subprocess import check_output

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
