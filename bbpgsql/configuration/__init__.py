from ConfigParser import SafeConfigParser
import os
from copy import deepcopy
import stat
import logging.config
from logging import (
#    DEBUG,
#    INFO,
    WARNING,
#    ERROR,
#    CRITICAL,
)
import socket
import logging

BBPGSQL_LOGGER_NAME = 'bbpgsql'

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


def get_config_from_filename_and_set_up_logging(filename):
    conf = config([filename])
    set_up_logging(conf)
    return conf


def write_config_to_filename(config_dictionary, config_filename):
    config = SafeConfigParser()
    for section in config_dictionary:
        config.add_section(section)
        variables = config_dictionary[section]
        for v in variables:
            config.set(section, v, variables[v])
    mode = stat.S_IRUSR | stat.S_IWUSR
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(config_filename, flags, mode)
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
    'loggers': {
        BBPGSQL_LOGGER_NAME: {
            'handlers': [],
        },
    },
    'formatters': {
    },
}


def get_log_level_from_string(level):
    return logging.getLevelName(level.upper())


def build_logging_configuration_dict(config):
    log_config = deepcopy(default_log_config)
    new_handlers = []
    bbpgsql_log_config = log_config['loggers'][BBPGSQL_LOGGER_NAME]
    if config.has_section('Logging'):
        if config.has_option('Logging', 'loglevel'):
            level = config.get('Logging', 'loglevel')
            lvl = logging.getLevelName(level.upper())
            if type(lvl) is not type(1):
                raise(Exception('Invalid Logging Level'))
            bbpgsql_log_config['level'] = lvl
        handlers, formatters = set_up_logger_file_handler(config)
        new_handlers.extend(handlers.keys())
        log_config['handlers'].update(handlers)
        log_config['formatters'].update(formatters)
        handlers, formatters = set_up_logger_syslog_handler(config)
        new_handlers.extend(handlers.keys())
        log_config['handlers'].update(handlers)
        log_config['formatters'].update(formatters)
        bbpgsql_log_config['handlers'] = list(
            set(bbpgsql_log_config['handlers'] + new_handlers))
    return log_config


def set_up_logging(config):
    log_config = build_logging_configuration_dict(config)
    logging.config.dictConfig(log_config)
    return log_config


def set_up_logger_file_handler(config):
    handlers = {}
    formatters = {}
    if config.has_section('Logging'):
        # create handler
        # add to logger
        # create formatter
        if config.has_option('Logging', 'logfile'):
            logfile = config.get('Logging', 'logfile')
            if config.has_option('Logging', 'loghistory'):
                loghistory = int(config.get('Logging', 'loghistory'))
            else:
                loghistory = 7
            formatters['file_formatter'] = {
                'format': "%(asctime)s - %(levelname)s - %(message)s",
            }
            handlers['file'] = {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'file_formatter',
                'filename': logfile,
                'when': 'd',
                'interval': 1,
                'backupCount': loghistory,
            }
    return handlers, formatters


def set_up_logger_syslog_handler(config):
    handlers = {}
    formatters = {}
    if config.has_section('Logging'):
        if config.has_option('Logging', 'loghost') and \
            config.has_option('Logging', 'logport'):
            log_host = config.get('Logging', 'loghost')
            log_port = int(config.get('Logging', 'logport'))
            log_address = (log_host, log_port)
            formatters['syslog_formatter'] = {
                'format': '%(asctime)s %(name)s: %(levelname)s %(message)s',
                'datefmt': '%b %e %H:%M:%S',
            }
            socktype = socket.SOCK_DGRAM
            if config.has_option('Logging', 'logtcp'):
                if config.getboolean('Logging', 'logtcp'):
                    socktype = socket.SOCK_STREAM
                else:
                    socktype = socket.SOCK_DGRAM
            facility = logging.handlers.SysLogHandler.LOG_USER
            if config.has_option('Logging', 'logfacility'):
                try:
                    facility = logging.handlers.SysLogHandler.facility_names[
                        config.get('Logging', 'logfacility')]
                except KeyError:
                    raise Exception('Invalid "logfacility" value of "%s"' %
                        config.get('Logging', 'logfacility'))
            handlers['syslog'] = {
                'class': 'logging.handlers.SysLogHandler',
                'formatter': 'syslog_formatter',
                'address': log_address,
                'facility': facility,
                'socktype': socktype,
            }
    return handlers, formatters
