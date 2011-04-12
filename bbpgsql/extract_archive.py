import tarfile


def extract_archive(archivePath, extractPath):
    tf = tarfile.open(archivePath)
    tf.extractall(path=extractPath)
