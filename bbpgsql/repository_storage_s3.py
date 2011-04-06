import os
from bbpgsql.repository_commit import BBCommit
from bbpgsql.repository_exceptions import FileAlreadyExistsError
from bbpgsql.repository_exceptions import UnknownTagError


class S3CommitStorage(object):
    tag_separator = '-'

    def __init__(self, bucket):
        self.bucket = bucket

    def __getitem__(self, tag):
        keyname = self._get_keyname_for_tag(tag)
        message = self._message_from_keyname(keyname)
        return BBCommit(self, tag, message)

    def __contains__(self, tag):
        return 0 < len([k for k in self.bucket.list(prefix=tag)])

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

    def add_commit(self, tag, fp, message):
        new_key_name = self.tag_separator.join([tag, message])
        new_key = self.bucket.new_key(new_key_name)
        new_key.set_contents_from_file(fp)

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

