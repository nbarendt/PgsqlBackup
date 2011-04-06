import os
from bbpgsql.repository_commit import BBCommit


class TagAlreadyExistsError(Exception):
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return 'Tag "{0}" already exists!'.format(self.tag)


class FileAlreadyExistsError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'File "{0}" already exists!'.format(self.filename)


class UnknownTagError(Exception):
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return 'Unknown Tag "{0}"!'.format(self.tag)


class S3CommitStorage(object):
    tag_separator = '-'

    def __init__(self, bucket):
        self.bucket = bucket

    def __getitem__(self, tag):
        keyname = self._get_keyname_for_tag(tag)
        message = self._message_from_keyname(keyname)
        return BBCommit(self, tag, message)

    def _tag_from_keyname(self, keyname):
        return keyname.split(self.tag_separator, 1)[0]

    def _message_from_keyname(self, keyname):
        return keyname.split(self.tag_separator, 1)[1]

    def _get_mapping_of_tags_to_keynames(self):
        keynames = self._get_commit_keynames()
        mapping = {}
        for key in keynames:
            mapping[self._tag_from_keyname(key)] = key
        return mapping

    def _get_keyname_for_tag(self, tag):
        try:
            return self._get_mapping_of_tags_to_keynames()[tag]
        except KeyError:
            raise UnknownTagError(tag)

    def _get_commit_keynames(self):
        return [k.name for k in self.bucket.list()]

    def add_commit(self, tag, filename, message):
        if tag in self.get_tags():
            raise TagAlreadyExistsError('Tag {0} already exists'.format(tag))
        new_key_name = self.tag_separator.join([tag, message])
        new_key = self.bucket.new_key(new_key_name)
        new_key.set_contents_from_filename(filename)

    def delete_commit(self, tag):
        keyname_to_delete = self._get_keyname_for_tag(tag)
        key_to_delete = self.bucket.get_key(keyname_to_delete)
        key_to_delete.delete()

    def get_tags(self):
        keys = self._get_commit_keynames()
        return [self._tag_from_keyname(key) for key in keys]

    def get_commit_contents_to_filename(self, tag, filename):
        if os.path.exists(filename):
            raise FileAlreadyExistsError(filename)
        keyname = self._get_keyname_for_tag(tag)
        key = self.bucket.get_key(keyname)
        key.get_contents_to_filename(filename)

    def get_message_for_tag(self, tag):
        keyname = self._get_keyname_for_tag(tag)
        return self._message_from_keyname(keyname)

