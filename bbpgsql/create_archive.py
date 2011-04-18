import tarfile


def create_archive(srcPath, archivePath, excludeDirs=None):
    fhandle = tarfile.open(name=archivePath, mode='w')
    fhandle.add(srcPath, arcname='.')
    fhandle.close()
