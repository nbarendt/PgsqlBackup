class DuplicateTagError(Exception):
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        msg = 'DuplicateTagError: the tag "{0}" already exists in' \
              ' the repository'.format(self.tag)
        return msg


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

