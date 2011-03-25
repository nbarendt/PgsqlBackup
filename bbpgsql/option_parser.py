from optparse import OptionParser
import os


def parse_args(args=None):
    parser = OptionParser()
    parser.add_option('-c', '--config', dest='config_file',
        help='configuration file', default='/etc/bbpgsql.ini')
    options, args = parser.parse_args(args)
    return options, args


def validate_options_and_args(options=None, args=None):
    if not os.path.exists(options.config_file):
        raise Exception("File %s does not exist" % (options.config_file))
