class BBCommit(object):
    def __init__(self, store, tag,  message):
        self.store = store
        self.tag = tag
        self.message = message

    def get_contents_to_filename(self, filename):
        self.store.get_commit_contents_to_filename(self.tag, filename)
