from unittest import TestCase
from bbpgsql.repository_commit import BBCommit
from mock import Mock


class TestBBCommit(TestCase):
    def setUp(self):
        self.mock_store = Mock()
        self.commit = BBCommit(self.mock_store, 'tag1', 'msg1')

    def test_tag_and_message_properties(self):
        self.assertEqual('tag1', self.commit.tag)
        self.assertEqual('msg1', self.commit.message)

    def test_commit_get_contents_to_file_passes_tag_and_filename(self):
        self.commit.get_contents_to_filename('somefile')
        self.mock_store.get_commit_contents_to_filename.assert_called_with(
            'tag1', 'somefile')
