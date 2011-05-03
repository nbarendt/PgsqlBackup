from ConfigParser import SafeConfigParser

"""
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
"""
