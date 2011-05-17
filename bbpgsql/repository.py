from re import match
from bbpgsql.repository_exceptions import DuplicateTagError

CHARACTER_REGEX = r'^[a-zA-Z0-9\-\:\.]*$'


class BBRepository(object):
    character_regex = CHARACTER_REGEX

    def __init__(self, store):
        self.store = store

    def _get_commit_by_tag(self, tag):
        return self.store[tag]

    def __iter__(self):
        for tag in self._sorted_tags():
            yield self._get_commit_by_tag(tag)

    def __getitem__(self, tag):
        return self._get_commit_by_tag(tag)

    def _sorted_tags(self):
        return sorted(self.store.get_tags())

    def _tag_is_unique(self, tag):
        if tag in self.store:
            raise DuplicateTagError(tag)

    def _message_is_legal(self, message):
        if message and not match(self.character_regex, message):
            raise Exception('Message "{0}" does not match regex "{1}"'.format(
                message, self.character_regex))

    def _tag_is_legal(self, tag):
        if not tag or not match(self.character_regex, tag):
            raise Exception('Tag "{0}" does not match regex "{1}"'.format(
                tag, self.character_regex))

    def create_commit_from_filename(self, tag, filename, message=None):
        message = message or ''
        try:
            self._tag_is_unique(tag)
            self._tag_is_legal(tag)
            self._message_is_legal(message)
            self.store.add_commit(tag, open(filename, 'rb'), message)
        except DuplicateTagError:
            commit = self[tag]
            if not commit.contents_are_identical_to_filename(filename):
                raise

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
