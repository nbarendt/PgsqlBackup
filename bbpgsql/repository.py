from re import match
import os

CHARACTER_REGEX = r'^[a-zA-Z0-9\_]*$'


class DuplicateTagError(Exception):
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        msg = 'DuplicateTagError: the tag "{0}" already exists in' \
              ' the repository'.format(self.tag)
        return msg


class BBCommit(object):
    def __init__(self, tag, contents, message):
        self.tag = tag
        self.contents = contents
        self.message = message

    def get_to_filename(self, filename):
        open(filename, 'wb').write(self.contents)


class MemoryCommitStorage(object):

    def __init__(self):
        self.data = {}

    def add_commit(self, tag, contents, message):
        self.data[tag] = dict(data=contents, message=message)          

    def delete_commit(self, tag):
        del self.data[tag]

    def get_tags(self):
        return self.data.keys()

    def get_contents_for_tag(self, tag):
        return self.data[tag]['data']

    def get_message_for_tag(self, tag):
        return self.data[tag]['message']


class FilesystemCommitStorage(object):
    tag_separator = '-'

    def __init__(self, directory):
        self.path_to_storage = directory

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

    def get_contents_for_tag(self, tag):
        return open(self._tag_to_absolute_path(tag), 'rb').read()

    def get_message_for_tag(self, tag):
        commit_file = self._get_commits()[tag]
        return self._get_message_from_commit_filename(commit_file)


class BBRepository(object):
    character_regex = CHARACTER_REGEX

    def __init__(self, store):
        self.store = store

    def _get_commit_by_tag(self, tag):
        return BBCommit(tag,
             self.store.get_contents_for_tag(tag),
            self.store.get_message_for_tag(tag))

    def __iter__(self):
        for tag in self._sorted_tags():
            yield self._get_commit_by_tag(tag)

    def __getitem__(self, tag):
        return self._get_commit_by_tag(tag)

    def _sorted_tags(self):
        return sorted(self.store.get_tags())

    def _tag_is_unique(self, tag):
        if tag in self.store.get_tags():
            raise DuplicateTagError(tag)

    def _message_is_legal(self, message):
        if message and not match(self.character_regex, message):
            raise Exception('Message "{0}" does not match regex "{1}"'.format(
                message, self.character_regex))

    def _tag_is_legal(self, tag):
        if not match(self.character_regex, tag):
            raise Exception('Tag "{0}" does not match regex "{1}"'.format(
                tag, self.character_regex))

    def create_commit_from_filename(self, tag, filename, message=None):
        message = message or ''
        self._tag_is_unique(tag)
        self._tag_is_legal(tag)
        self._message_is_legal(message)
        self.store.add_commit(tag, open(filename, 'rb').read(), message)

    def delete_commits_before(self, new_oldest_commit):
        new_oldest_tag = new_oldest_commit.tag
        tags_to_delete = [k for k in self._sorted_tags() if k < new_oldest_tag]
        for tag in tags_to_delete:
            self.store.delete_commit(tag)

    def get_commit_before(self, commit_N):
        tags = self._sorted_tags()
        N_minus_1 = tags.index(commit_N.tag) - 1
        if N_minus_1 < 0:
            raise ValueError()
        return self[tags[N_minus_1]]
