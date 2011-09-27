from tempfile import mkdtemp, template
from shutil import rmtree
from os.path import exists


# borrowing from Python 3
class TemporaryDirectory:
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everthing contained
    in it are removed.
    """

    def __init__(self, suffix="", prefix=template, dir=None):
        self.name = mkdtemp(suffix, prefix, dir)

    def __enter__(self):
        return self.name

    def cleanup(self):
        if exists(self.name):
            rmtree(self.name)

    def __exit__(self, exc, value, tb):
        self.cleanup()
