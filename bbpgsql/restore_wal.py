#from bbpgsql.configuration.repository import get_WAL_repository


class Restore_WAL(object):
    def __init__(self, repository):
        self.repository = repository

    def restore(self, basename, destination):
        commit = self.repository[basename]
        commit.get_contents_to_filename(destination)
