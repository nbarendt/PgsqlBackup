from unittest import TestCase
from bbpgsql.repository_commit import BBCommit
from mock import Mock, patch, sentinel


class TestBBCommit(TestCase):
    def setUp(self):
        self.mock_store = Mock()
        self.commit = BBCommit(self.mock_store, 'tag1', 'msg1', 'abcdef')

    def test_tag_and_message_properties(self):
        self.assertEqual('tag1', self.commit.tag)
        self.assertEqual('msg1', self.commit.message)

    def test_commit_get_contents_to_file_passes_tag_and_filename(self):
        self.commit.get_contents_to_filename('somefile')
        self.mock_store.get_commit_contents_to_filename.assert_called_with(
            'tag1', 'somefile')

    @patch('__builtin__.open')
    def test_commit_can_compare_filename_to_content_fingerprint_successfully(
            self,
            mock_open):
        self.mock_store.get_fingerprint_for_file.return_value = 'abcdef'
        mock_open.return_value = sentinel.open
        self.assertTrue(self.commit.contents_are_identical_to_filename(
            'filename'))
        self.mock_store.get_fingerprint_for_file.assert_called_once_with(
            sentinel.open)

    @patch('__builtin__.open')
    def test_commit_can_compare_filename_to_content_fingerprint_unsuccessfully(
            self,
            mock_open):
        self.mock_store.get_fingerprint_for_file.return_value = 'abcdef'[::-1]
        mock_open.return_value = sentinel.open
        self.assertFalse(self.commit.contents_are_identical_to_filename(
            'filename'))
        self.mock_store.get_fingerprint_for_file.assert_called_once_with(
            sentinel.open)
