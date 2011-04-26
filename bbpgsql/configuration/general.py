from ConfigParser import NoOptionError


class MissingDataDirError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


SECTION_NAME = 'General'
DATA_DIR_KEY = 'pgsql_data_directory'


def get_data_dir(config):
    try:
        data_dir = config.get(SECTION_NAME, DATA_DIR_KEY)
    except NoOptionError:
        raise MissingDataDirError(
            'A {0} value must be provided in the {1} section.'.format(
                DATA_DIR_KEY, SECTION_NAME))
    return data_dir
