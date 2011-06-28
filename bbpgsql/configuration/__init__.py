from ConfigParser import SafeConfigParser
import os
import stat
import logging.config
from logging import (
#    DEBUG,
#    INFO,
    WARNING,
#    ERROR,
#    CRITICAL,
)


default_configuration = {
    'General': {
    },
    'WAL': {
        'driver': 's3',
    },
    'Snapshot': {
        'driver': 's3',
    },
    'Credentials': {
    },
}


def configure_defaults(config_parser):
    for section in default_configuration:
        config_parser.add_section(section)
        section_keys = default_configuration[section]
        for key in section_keys:
            config_parser.set(section, key, section_keys[key])


def config(filenames=None):
    filenames = filenames or []
    config_parser = SafeConfigParser()
    configure_defaults(config_parser)
    config_parser.read(filenames)
    return config_parser


def get_config_from_filename(filename):
    return config([filename])


def write_config_to_filename(config_dictionary, config_filename):
    config = SafeConfigParser()
    for section in config_dictionary:
        config.add_section(section)
        variables = config_dictionary[section]
        for v in variables:
            config.set(section, v, variables[v])
    mode = stat.S_IRUSR | stat.S_IWUSR
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    print('opening file {0} with flags {1} and mode {2}'.format(
        config_filename, flags, mode))
    fd = os.open(config_filename, flags, mode)
    print('file descriptor is: {0}'.format(fd))
    f = os.fdopen(fd, 'wb')
    config.write(f)
    f.close()


default_log_config = {
    'version': 1,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'level': WARNING,
        'handlers': ['null'],
    },
}


def get_log_level_from_string(level):
        return getattr(logging, level)


def set_up_logging(config):
    logging.config.dictConfig(default_log_config)
    logger = logging.getLogger()
    if config.has_section('Logging'):
        if config.has_option('Logging', 'level'):
            level = config.get('Logging', 'level')
            print(level)
            logger.setLevel(get_log_level_from_string(level))


def set_up_logger_file_handler(filename):
    return logging.handlers.TimedRotatingFileHandler(filename)
