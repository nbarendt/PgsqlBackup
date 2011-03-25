import tarfile

directory_to_archive = '/home/markdohring/projects'
archive_name = '/home/markdohring/projects.tar.gz'

# Open a tar file for writing with gzip compression
tf_obj=tarfile.open(name=archive_name, mode='w:gz')
tf_obj.add(directory_to_archive)
tf_obj.close()

tf_obj=tarfile.open(name=archive_name, mode='r:gz')
tf_obj.list(verbose=True)


