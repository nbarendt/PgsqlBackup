#import os
from bbpgsql.repository_commit import BBCommit


class MemoryCommitStorage(object):
    def __init__(self):
        self.data = {}

    def __contains__(self, tag):
        return tag in self.data

    def __getitem__(self, tag):
        return BBCommit(self, tag, self.get_message_for_tag(tag))

    def add_commit(self, tag, fp, message):
        self.data[tag] = dict(data=fp.read(), message=message)

    def delete_commit(self, tag):
        del self.data[tag]

    def get_tags(self):
        return self.data.keys()

    def get_commit_contents_to_filename(self, tag, filename):
        open(filename, 'wb').write(self.data[tag]['data'])

    def get_message_for_tag(self, tag):
        return self.data[tag]['message']
