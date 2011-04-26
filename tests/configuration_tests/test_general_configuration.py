from unittest import TestCase
from bbpgsql.configuration import config
from bbpgsql.configuration.general import (
    get_data_dir,
    MissingDataDirError,
    )

class Test_General_data_dir(TestCase):
    def setUp(self):
        self.config = config()

    def test_will_raise_MissingDataDirError(self):

        def will_raise_MissingDataDirError():
            get_data_dir(self.config)

        self.assertRaises(MissingDataDirError,
            will_raise_MissingDataDirError)
