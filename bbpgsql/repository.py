from re import match

CHARACTER_REGEX = r'^[a-zA-Z0-9\_]*$'


class DuplicateTagError(Exception):
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        msg = 'DuplicateTagError: the tag "{0}" already exists in' \
              ' the repository'.format(self.tag)
        return msg


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
        self.store.add_commit(tag, filename, message)

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
