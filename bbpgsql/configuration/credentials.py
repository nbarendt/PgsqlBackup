from ConfigParser import NoOptionError
from boto import connect_s3


class MissingCredentialsError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


SECTION_NAME = 'Credentials'
ACCESS_KEY_NAME = 'aws_access_key_id'
SECRET_KEY_NAME = 'aws_secret_key_id'


def get_aws_credentials(config):
    try:
        access_key = config.get(SECTION_NAME, 'aws_access_key_id')
    except NoOptionError:
        raise MissingCredentialsError(
            'A {0} value must be provided in the {1} section.'.format(
                ACCESS_KEY_NAME, SECTION_NAME))

    try:
        secret_key = config.get(SECTION_NAME, 'aws_secret_key_id')
    except NoOptionError:
        raise MissingCredentialsError(
            'A {0} value must be provided in the {1} section.'.format(
                SECRET_KEY_NAME, SECTION_NAME))

    return access_key, secret_key


def get_s3_connection(access_key, secret_key):
    return connect_s3(access_key, secret_key)
