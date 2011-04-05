import os

class BBCommit(object):
    def __init__(self, store, tag,  message):
        self.store = store
        self.tag = tag
        self.message = message

    def get_contents_to_filename(self, filename):
        self.store.get_commit_contents_to_filename(self.tag, filename)


class MemoryCommitStorage(object):
    def __init__(self):
        self.data = {}

    def __getitem__(self, tag):
        return BBCommit(self, tag, self.get_message_for_tag(tag))

    def add_commit(self, tag, contents, message):
        self.data[tag] = dict(data=contents, message=message)

    def delete_commit(self, tag):
        del self.data[tag]

    def get_tags(self):
        return self.data.keys()

    def get_contents_for_tag(self, tag):
        return self.data[tag]['data']

    def get_commit_contents_to_filename(self, tag, filename):
        open(filename, 'wb').write(self.data[tag]['data'])

    def get_message_for_tag(self, tag):
        return self.data[tag]['message']


class FilesystemCommitStorage(object):
    tag_separator = '-'

    def __init__(self, directory):
        self.path_to_storage = directory

    def __getitem__(self, tag):
        return BBCommit(self, tag, self.get_message_for_tag(tag))

    def _commit_filename_to_absolute_path(self, commit_filename):
        return os.path.join(self.path_to_storage, commit_filename)

    def _tag_to_absolute_path(self, tag):
        commit_filename = self._get_commits()[tag]
        return self._commit_filename_to_absolute_path(commit_filename)

    def _get_list_of_commit_files(self):
        return os.listdir(self.path_to_storage)

    def _get_commits(self):
        commits = {}
        for commit_filename in self._get_list_of_commit_files():
            tag = self._get_tag_from_commit_filename(commit_filename)
            commits[tag] = commit_filename
        return commits

    def _get_tag_from_commit_filename(self, commit_filename):
        return commit_filename.split(self.tag_separator, 1)[0]

    def _get_message_from_commit_filename(self, commit_filename):
        return commit_filename.split(self.tag_separator, 1)[1]

    def add_commit(self, tag, contents, message):
        commit_filename = self.tag_separator.join([tag, message])
        commit_path = self._commit_filename_to_absolute_path(commit_filename)
        open(commit_path, 'wb').write(contents)

    def delete_commit(self, tag):
        os.remove(self._tag_to_absolute_path(tag))

    def get_tags(self):
        return self._get_commits().keys()

    def get_commit_contents_to_filename(self, tag, filename):
        return open(filename, 'wb').write(
            open(self._tag_to_absolute_path(tag), 'rb').read())

    def get_message_for_tag(self, tag):
        commit_file = self._get_commits()[tag]
        return self._get_message_from_commit_filename(commit_file)

