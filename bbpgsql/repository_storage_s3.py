import os
from bbpgsql.repository_commit import BBCommit
from bbpgsql.repository_exceptions import FileAlreadyExistsError
from bbpgsql.repository_exceptions import UnknownTagError


class KeynameTagMessageMapper(object):
    def __init__(self, bucket_prefix, tag_separator,
            keyname=None,
            tag=None, message=None):
        if keyname and (tag or message):
            raise Exception('Only keyname or tag & message should be provided')
        self.tag_separator = tag_separator
        self.bucket_prefix = bucket_prefix
        self.bucket_prefix_len = len(bucket_prefix)
        self._keyname = keyname or ''
        self._tag = tag or ''
        self._message = message or ''

    def _strip_prefix(self, keyname):
        return keyname[self.bucket_prefix_len:]
    
    def tag_from_keyname(self):
        return self._strip_prefix(self._keyname).split(self.tag_separator, 1)[0]

    def message_from_keyname(self):
        return self._strip_prefix(self._keyname).split(self.tag_separator, 1)[1]

    def keyname_from_tag_and_message(self):
        return ''.join([self.bucket_prefix, self._tag, self.tag_separator,
            self._message])

    @property
    def tag(self):
        return self._tag or self.tag_from_keyname()

    @property
    def message(self):
        return self._message or self.message_from_keyname()

    @property
    def keyname(self):
        return self._keyname or self.keyname_from_tag_and_message()


class S3CommitStorage(object):
    tag_separator = '-'

    def __init__(self, bucket, prefix=None):
        self.bucket = bucket
        self.bucket_prefix = prefix or ''
        if self.bucket_prefix.startswith('/'):
            raise Exception('Bucket prefix must not start with leading slash')
        self.bucket_prefix_len = len(self.bucket_prefix)

    def _get_keyname_mapper(self, keyname=None, tag=None, message=None):
        return KeynameTagMessageMapper(self.bucket_prefix,
            self.tag_separator, keyname, tag, message)

    def __getitem__(self, tag):
        keyname = self._get_keyname_mapper(self._get_keyname_for_tag(tag))
        return BBCommit(self, keyname.tag, keyname.message)

    def __contains__(self, tag):
        return 0 < len(self._get_keys_that_start_with_tag(tag))

    def _get_commit_keynames(self):
        return [k.name for k in self.bucket.list(prefix=self.bucket_prefix)]

    def _get_keys_that_start_with_tag(self, tag):
        search_prefix = self._get_keyname_mapper(tag=tag).keyname
        return [k.name for k in self.bucket.list(prefix=search_prefix)]

    def _get_mapping_of_tags_to_keynames(self):
        keynames = self._get_commit_keynames()
        mapping = {}
        for key in keynames:
            mapping[self._get_keyname_mapper(key).tag] = key
        return mapping

    def _get_keyname_for_tag(self, tag):
        keynames = self._get_keys_that_start_with_tag(tag)
        if len(keynames) == 1:
            return keynames[0]
        else:
            raise UnknownTagError(tag)

    def add_commit(self, tag, fp, message):
        new_key_name = self._get_keyname_mapper(tag=tag, message=message).keyname
        new_key = self.bucket.new_key(new_key_name)
        new_key.set_contents_from_file(fp)

    def delete_commit(self, tag):
        keyname_to_delete = self._get_keyname_for_tag(tag)
        key_to_delete = self.bucket.get_key(keyname_to_delete)
        key_to_delete.delete()

    def get_tags(self):
        keys = self._get_commit_keynames()
        return [self._get_keyname_mapper(key).tag for key in keys]

    def get_commit_contents_to_filename(self, tag, filename):
        if os.path.exists(filename):
            raise FileAlreadyExistsError(filename)
        keyname = self._get_keyname_for_tag(tag)
        key = self.bucket.get_key(keyname)
        key.get_contents_to_filename(filename)

    def get_message_for_tag(self, tag):
        keyname = self._get_keyname_for_tag(tag)
        return self._get_keyname_mapper(keyname).message

