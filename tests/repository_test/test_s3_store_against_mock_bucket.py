from unittest import TestCase
from testfixtures import TempDirectory
from bbpgsql.repository_storage_s3 import S3CommitStorage
from bbpgsql.repository_storage_s3 import FileAlreadyExistsError
from bbpgsql.repository_storage_s3 import UnknownTagError
from mock import Mock
from boto.s3.bucket import Bucket
from boto.s3.key import Key


class Test_S3CommitStorage_Against_Mock(TestCase):
    def setUp(self):
        self.tempdir = TempDirectory()
        self.setup_mock_defaults()
        self.store = S3CommitStorage(self.mock_bucket)
    
    def setup_mock_defaults(self):
        self.mock_bucket = Mock(spec=Bucket)
        self.set_bucket_list([])

    def tearDown(self):
        self.tempdir.cleanup()

    def set_bucket_list(self, keynames):
        key_objs = [Key(None, key) for key in keynames]
        self.mock_bucket.list.return_value = key_objs

    def test_get_tags_calls_bucket_list__empty(self):
        self.assertEqual([], self.store.get_tags())
        self.mock_bucket.list.assert_called_with()

    def test_get_tags_calls_bucket_list_not_empty(self):
        self.set_bucket_list(['tag1-msg1', 'tag2-msg2'])
        self.store.get_tags()
        self.mock_bucket.list.assert_called_with()

    def test_get_tags_parses_keys_properly(self):
        self.set_bucket_list(['tag1-msg1', 'tag2-msg2'])
        self.assertEqual(['tag1', 'tag2'], self.store.get_tags())

    def test_get_message_for_tag_calls_bucket_list(self):
        self.set_bucket_list(['tag1-msg1'])
        self.store.get_message_for_tag('tag1')
        self.mock_bucket.list.assert_called_with()

    def test_get_message_for_tag_parses_keyname_properly(self):
        self.set_bucket_list(['tag1-msg1'])
        self.assertEqual('msg1', self.store.get_message_for_tag('tag1'))

    def test_add_commit_calls_new_key_with_expected_format(self):
        file1 = self.tempdir.write('file1', 'some file contents')
        self.store.add_commit('tag1', file1, 'some_message')
        expected_key_name = '-'.join(['tag1', 'some_message'])
        self.mock_bucket.new_key.assert_called_with(expected_key_name)

    def test_add_commit_calls_set_contents_from_filename(self):
        file1 = self.tempdir.write('file1', 'some file contents')
        self.store.add_commit('tag1', file1, 'some_message')
        new_key_mock = self.mock_bucket.new_key.return_value
        new_key_mock.set_contents_from_filename.assert_called_with(file1)

    def test_delete_commit_calls_get_key(self):
        self.set_bucket_list(['tag1-msg1'])
        self.store.delete_commit('tag1')
        self.mock_bucket.get_key.assert_called_with('tag1-msg1')
        self.mock_bucket.get_key.return_value.delete.assert_called_with()

    def test_get_commit_contents_calls_get_contents_to_filename(self):
        self.set_bucket_list(['tag1-msg1'])
        target_file = self.tempdir.getpath('restored_file')
        self.store.get_commit_contents_to_filename('tag1', target_file)
        get_key = self.mock_bucket.get_key.return_value
        get_key.get_contents_to_filename.assert_called_with(target_file)

    def test_get_commit_contents_raises_Exception_if_file_exists(self):
        self.set_bucket_list(['tag1-msg1'])
        file1 = self.tempdir.write('file1', 'some file contents')
        
        def will_raise_Exception():
            self.store.get_commit_contents_to_filename('tag1', file1)
        self.assertRaises(FileAlreadyExistsError, will_raise_Exception)

    def test_dictionary_interface_returns_a_commit_object(self):
        self.set_bucket_list(['tag1-msg1'])
        commit = self.store['tag1']
        self.assertEqual('tag1', commit.tag)
        self.assertEqual('msg1', commit.message)

    def test_dictionary_interface_raises_Exception_if_unknown_tag(self):

        def will_raise_UnknownTagError():
            self.store['tag1']
        self.assertRaises(UnknownTagError, will_raise_UnknownTagError)

    def test_contains_interface_calls_bucket_list_with_prefix(self):
        self.set_bucket_list(['tag1-msg1'])
        'tag1' in self.store
        self.mock_bucket.list.assert_called_with(prefix='tag1')

    def test_contains_interface_returns_true_for_tags_in_bucket(self):
        self.set_bucket_list(['tag1-msg1'])
        self.assertTrue('tag1' in self.store)

    def test_contains_interface_returns_false_for_tags_not_in_bucket(self):
        self.assertFalse('tag2' in self.store)

