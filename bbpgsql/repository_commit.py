class BBCommit(object):
    def __init__(self, store, tag,  message, fingerprint):
        self.store = store
        self.tag = tag
        self.message = message
        self.fingerprint = fingerprint

    def get_contents_to_filename(self, filename):
        self.store.get_commit_contents_to_filename(self.tag, filename)

    def contents_are_identical_to_filename(self, filename):
        file_fingerprint = self.store.get_fingerprint_for_file(
            open(filename, 'rb'))
        print("self.fingerprint", self.fingerprint)
        return file_fingerprint == self.fingerprint
