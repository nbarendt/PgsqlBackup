from unittest import TestCase
from bbpgsql.repository_exceptions import DuplicateTagError
from bbpgsql.repository_exceptions import FileAlreadyExistsError
from bbpgsql.repository_exceptions import UnknownTagError


class Test_DuplicateTagError(TestCase):
    def test_str_output(self):
        expected = 'DuplicateTagError: the tag "badtag" already' \
                    ' exists in the repository'
        self.assertEqual(expected, str(DuplicateTagError('badtag')))


class Test_FileAlreadyExistsError(TestCase):
    def test_str_output(self):
        expected = 'File "somefile" already exists!'
        self.assertEqual(expected, str(FileAlreadyExistsError('somefile')))


class Test_UnknownTagError(TestCase):
    def test_str_output(self):
        expected = 'Unknown Tag "sometag"!'
        self.assertEqual(expected, str(UnknownTagError('sometag')))
