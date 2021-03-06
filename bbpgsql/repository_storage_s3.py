import os
from bbpgsql.repository_commit import BBCommit
from bbpgsql.repository_exceptions import FileAlreadyExistsError
from bbpgsql.repository_exceptions import UnknownTagError
from gzip import GzipFile
from shutil import copyfileobj
from tempfile import mkstemp
from hashlib import md5


FINGERPRINT_METADATA_KEY = 'fingerprint'
CUSTOM_HTTP_FINGERPRINT_HEADER = ''.join(['x-amz-meta-',
     FINGERPRINT_METADATA_KEY])


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

    def _get_key_part(self, part_number):
        stripped_keyname = self._strip_prefix(self._keyname)
        parts = stripped_keyname.split(self.tag_separator, 1)
        return parts[part_number]

    def tag_from_keyname(self):
        return self._get_key_part(0)

    def message_from_keyname(self):
        return self._get_key_part(1)

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
    tag_separator = '_'

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
        keyname = self._get_keyname_for_tag(tag)
        keyname_mapper = self._get_keyname_mapper(keyname)
        key = self.bucket.get_key(keyname)
        return BBCommit(self, keyname_mapper.tag,
            keyname_mapper.message, key.get_metadata(
                FINGERPRINT_METADATA_KEY))

    def __contains__(self, tag):
        return 0 < len(self._get_keys_that_start_with_tag(tag))

    def _get_keynames_that_start_with(self, prefix):
        return [k.name for k in self.bucket.list(prefix=prefix)]

    def _get_commit_keynames(self):
        return self._get_keynames_that_start_with(self.bucket_prefix)

    def _get_keys_that_start_with_tag(self, tag):
        search_prefix = self._get_keyname_mapper(tag=tag).keyname
        return self._get_keynames_that_start_with(search_prefix)

    def _get_mapping_of_tags_to_keynames(self):
        keynames = self._get_commit_keynames()
        mapping = {}
        for keyname in keynames:
            mapping[self._get_keyname_mapper(keyname).tag] = keyname
        return mapping

    def _get_keyname_for_tag(self, tag):
        keynames = self._get_keys_that_start_with_tag(tag)
        if len(keynames) == 1:
            return keynames[0]
        else:
            raise UnknownTagError(tag)

    def add_commit(self, tag, fp, message):
        new_key_name = self._get_keyname_mapper(tag=tag,
            message=message).keyname
        new_key = self.bucket.new_key(new_key_name)
        self._gzip_file_to_key(new_key, fp)

    def delete_commit(self, tag):
        keyname_to_delete = self._get_keyname_for_tag(tag)
        key_to_delete = self.bucket.get_key(keyname_to_delete)
        key_to_delete.delete()

    def get_tags(self):
        keys = self._get_commit_keynames()
        return [self._get_keyname_mapper(key).tag for key in keys]

    def _gzip_file_to_key(self, key, fp):
        tmp_gzip_fp, tmp_gzip_filename = mkstemp()
        try:
            gzip_fp = GzipFile(mode='wb', fileobj=os.fdopen(tmp_gzip_fp, 'wb'))
            copyfileobj(fp, gzip_fp)
            gzip_fp.close()
            key.set_contents_from_file(
                open(tmp_gzip_filename, 'rb'),
                headers={
                'Content-Type': 'application/octet-stream',
                'Content-Encoding': 'gzip',
                CUSTOM_HTTP_FINGERPRINT_HEADER: self.get_fingerprint_for_file(
                    fp)
                })
        finally:
            os.remove(tmp_gzip_filename)

    def _gunzip_key_to_filename(self, key, filename):
        tmp_gunzip_fp, tmp_gunzip_filename = mkstemp()
        try:
            os.close(tmp_gunzip_fp)
            key.get_contents_to_filename(tmp_gunzip_filename)
            gzip_fp = GzipFile(tmp_gunzip_filename)
            copyfileobj(gzip_fp, open(filename, 'wb'))
        finally:
            os.remove(tmp_gunzip_filename)

    def get_commit_contents_to_filename(self, tag, filename):
        if os.path.exists(filename):
            raise FileAlreadyExistsError(filename)
        keyname = self._get_keyname_for_tag(tag)
        key = self.bucket.get_key(keyname)
        if key.content_encoding and key.content_encoding.lower() == 'gzip':
            self._gunzip_key_to_filename(key, filename)
        else:
            key.get_contents_to_filename(filename)

    def get_message_for_tag(self, tag):
        keyname = self._get_keyname_for_tag(tag)
        return self._get_keyname_mapper(keyname).message

    def get_fingerprint_for_file(self, file):
        file.seek(0)
        m = md5()
        for l in file:
            m.update(l)
        return m.hexdigest()

    def get_storage_size(self):
        return sum(k.size for k in self.bucket.list(prefix=self.bucket_prefix))
