import tarfile


def create_archive(srcPath, archivePath, excludeDirs=None):
    excludeDirs = excludeDirs or []
#    my_exclude = generate_exclude(excludeDirs)
    fhandle = tarfile.open(name=archivePath, mode='w')
#    fhandle.add(srcPath, arcname='.', filter=my_exclude)
    fhandle.add(srcPath, arcname='.')
    fhandle.close()

def generate_exclude(excludeDirs):
    def my_exclude():
        pass
    return my_exclude
'''
    def my_exclude(tarinfo):
        for excluded_name in excludeDirs:
            if tarinfo.name == excluded_name:
                return None
        return tarinfo
    return my_exclude
'''

