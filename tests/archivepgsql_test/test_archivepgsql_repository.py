from unittest import TestCase
from bbpgsql.repository import BBRepository
from bbpgsql.repository_storage_memory import MemoryCommitStorage
from testfixtures import TempDirectory
from bbpgsql.archive_pgsql import generate_tag, commit_snapshot_to_repository
from bbpgsql.archive_pgsql import get_first_WAL, get_last_WAL


class Test_Snapshot_Tag(TestCase):
    def test_can_get_a_tag(self):
        self.assertTrue(generate_tag())


class Test_SnapshotArchive_Repository(TestCase):
    def setUp(self):
        store = MemoryCommitStorage()
        self.repo = BBRepository(store)
        self.tempdir = TempDirectory()
        self.setup_archive_a_snapshot()

    def setup_archive_a_snapshot(self):
        archive_name = 'somearchive.tgz'
        self.archive_contents = '123'
        self.archive_path = self.tempdir.write(archive_name,
            self.archive_contents)
        self.tag = generate_tag()
        self.first_WAL = '01234'
        self.last_WAL = '45678'
        commit_snapshot_to_repository(self.repo, self.archive_path, self.tag,
            self.first_WAL, self.last_WAL)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_can_retrieve_snapshot_contents_with_tag(self):
        commit = [i for i in self.repo][-1]
        restore_path = self.tempdir.getpath('restorearchive.tgz')
        commit.get_contents_to_filename(restore_path)
        self.assertEqual(self.archive_contents,
            open(restore_path, 'rb').read())

    def test_get_first_WAL_file_for_archived_snapshot_with_tag(self):
        self.assertEqual(self.first_WAL, get_first_WAL(self.repo, self.tag))

    def test_get_last_WAL_file_for_archived_snapshot_with_tag(self):
        self.assertEqual(self.last_WAL, get_last_WAL(self.repo, self.tag))
