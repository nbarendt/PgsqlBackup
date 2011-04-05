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


class BBMemoryRepository(object):
    character_regex = CHARACTER_REGEX

    def __init__(self):
        self.data = {}

    def _get_commit_by_tag(self, tag):
        return BBCommit(tag, self.data[tag]['data'],
            self.data[tag]['message'])

    def __iter__(self):
        for tag in self._sorted_tags():
            yield self._get_commit_by_tag(tag)

    def __getitem__(self, tag):
        return self._get_commit_by_tag(tag)

    def _sorted_tags(self):
        return sorted(self.data.keys())

    def _tag_is_unique(self, tag):
        if tag in self.data:
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
        self.data[tag] = dict(data=open(filename, 'rb').read(),
                                message=message)

    def delete_commits_before(self, new_oldest_commit):
        new_oldest_tag = new_oldest_commit.tag
        tags_to_delete = [k for k in self._sorted_tags() if k < new_oldest_tag]
        for tag in tags_to_delete:
            del self.data[tag]

    def get_commit_before(self, commit_N):
        tags = self._sorted_tags()
        N_minus_1 = tags.index(commit_N.tag) - 1
        if N_minus_1 < 0:
            raise ValueError()
        return self[tags[N_minus_1]]


class BBFilesystemRepository(object):
    character_regex = CHARACTER_REGEX
    tag_separator = '-'

    def __init__(self, directory):
        self.path_to_repo = directory

    def _get_commit_by_tag(self, tag):
        commit_filename = self._get_commits()[tag]
        message = self._get_message_from_commit_filename(commit_filename)
        path_to_commit_filename = os.path.join(self.path_to_repo,
            commit_filename)
        return BBCommit(tag, open(path_to_commit_filename, 'rb').read(),
            message)

    def __iter__(self):
        for tag in self._sorted_tags():
            yield self._get_commit_by_tag(tag)

    def __getitem__(self, tag):
        return self._get_commit_by_tag(tag)

    def _get_list_of_commit_files(self):
        print os.listdir(self.path_to_repo)
        return os.listdir(self.path_to_repo)

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

    def _sorted_tags(self):
        tags = []
        for commit_file in self._get_list_of_commit_files():
            tags.append(self._get_tag_from_commit_filename(commit_file))
        return sorted(tags)

    def _tag_is_unique(self, tag):
        if tag in self._sorted_tags():
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
        commit_file = self.tag_separator.join([tag, message])
        commit_path = os.path.join(self.path_to_repo, commit_file)
        print("opening ", commit_path)
        open(commit_path, 'wb').write(open(filename, 'rb').read())

    def delete_commits_before(self, new_oldest_commit):
        new_oldest_tag = new_oldest_commit.tag
        tags_to_delete = [k for k in self._sorted_tags() if k < new_oldest_tag]
        for tag in tags_to_delete:
            commit_filename = os.path.join(self.path_to_repo,
                self._get_commits()[tag])
            os.remove(commit_filename)

    def get_commit_before(self, commit_N):
        tags = self._sorted_tags()
        N_minus_1 = tags.index(commit_N.tag) - 1
        if N_minus_1 < 0:
            raise ValueError()
        return self[tags[N_minus_1]]

