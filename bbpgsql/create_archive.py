import tarfile


def create_archive(srcPath, archivePath):
    fhandle = tarfile.open(name=archivePath, mode='w')
    fhandle.add(srcPath, arcname='.')
    fhandle.close()
