from bbpgsql.repository_commit import BBCommit
from hashlib import md5


class MemoryCommitStorage(object):
    def __init__(self):
        self.data = {}

    def __contains__(self, tag):
        return tag in self.data

    def __getitem__(self, tag):
        return BBCommit(self, tag, self.get_message_for_tag(tag),
            self.get_fingerprint_for_tag(tag))

    def add_commit(self, tag, fp, message):
        contents = fp.read()
        fingerprint = md5(contents).hexdigest()
        self.data[tag] = dict(
            data=contents,
            message=message,
            fingerprint=fingerprint)

    def delete_commit(self, tag):
        del self.data[tag]

    def get_tags(self):
        return self.data.keys()

    def get_commit_contents_to_filename(self, tag, filename):
        open(filename, 'wb').write(self.data[tag]['data'])

    def get_message_for_tag(self, tag):
        return self.data[tag]['message']

    def get_fingerprint_for_tag(self, tag):
        return self.data[tag]['fingerprint']

    def get_fingerprint_for_file(self, file):
        m = md5()
        for l in file:
            m.update(l)
        return m.hexdigest()

    def get_storage_size(self):
        tags = self.get_tags()
        storage_size = 0
        for tag in tags:
            storage_size += len(self.data[tag]['data'])
        return storage_size
