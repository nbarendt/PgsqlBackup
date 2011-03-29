import os

def create_archive(srcPath, destPath, archiveName):
    archivePath = os.path.join(destPath, archiveName)
    fhandle = file(archivePath, 'a')
    fhandle.close()
