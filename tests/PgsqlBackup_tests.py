from bbpgsql.file_system_archive import create_file_system_archive


def setup():
    print "SETUP!"


def teardown():
    print "TEAR DOWN!"


def test_basic():
    print "I RAN!"


def test_create_file_system_archive():
    create_file_system_archive('archive.tar')
