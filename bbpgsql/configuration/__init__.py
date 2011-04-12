from ConfigParser import SafeConfigParser

default_configuration = {
    'WAL storage': {
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

