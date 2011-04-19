import tarfile
import os


def create_archive(srcPath, archivePath, excludeDirs=None):
    excludeDirs = excludeDirs or []
    my_exclude = generate_exclude(excludeDirs)
    fhandle = tarfile.open(name=archivePath, mode='w')
    fhandle.add(srcPath, arcname='.', filter=my_exclude)
    fhandle.close()

def generate_exclude(excludeObjs):
    def my_exclude(tarinfo):
        for excluded_name in excludeObjs:
            excluded_name = os.path.normpath(excluded_name)
            if os.path.normpath(tarinfo.name) == excluded_name:
                return None
        return(tarinfo)
    return my_exclude
