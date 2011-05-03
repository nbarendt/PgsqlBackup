from ConfigParser import SafeConfigParser

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
    f = open(config_filename, 'wb')
    config.write(f)
    f.close()
