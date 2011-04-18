from unittest import TestCase
import tarfile
from bbpgsql.exclude_files import exclude


class Test_exclude_files(TestCase):
    def setUp(self):
        self.excluded = tarfile.TarInfo(name="exclude_this")
        self.excluded_too = tarfile.TarInfo(name="exclude_this_too")
        self.kept = tarfile.TarInfo(name="keep_this")
        self.kept_too = tarfile.TarInfo(name="keep_this_too")
        pass

    def tearDown(self):
        pass

    def test_filter_excludes_a_member(self):
        self.assertEqual(None, exclude(self.excluded))

    def test_filter_keeps_a_member(self):
        self.assertEqual(self.kept, exclude(self.kept))

    def test_filter_excludes_a_different_member(self):
        self.assertEqual(None, exclude(self.excluded_too))

    def test_filter_keeps_a_different_member(self):
        self.assertEqual(self.kept_too, exclude(self.kept_too))
