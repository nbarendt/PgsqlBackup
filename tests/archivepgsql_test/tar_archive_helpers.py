from testfixtures import TempDirectory
import os


# Helper functions
def fill_directory_tree(topDir):
    # level 0 files
    topDir.write('file0', '')
    topDir.write('file1', '1')
    topDir.write('file2', '22')
    # level 0 directories
    topDir.makedir('dir0')
    topDir.makedir('dir1')
    topDir.makedir('dir2')
    # level 1 files
    topDir.write('dir1/file0', '')
    topDir.write('dir1/file1', '1')
    topDir.write('dir1/file2', '22')
    topDir.write('dir2/file0', '')
    topDir.write('dir2/file1', '1')
    topDir.write('dir2/file2', '22')
    # level 1 directories
    topDir.makedir('dir1/dir0')
    topDir.makedir('dir1/dir1')
    topDir.makedir('dir1/dir2')
    topDir.makedir('dir2/dir0')
    topDir.makedir('dir2/dir1')
    topDir.makedir('dir2/dir2')
    # level 2 files
    topDir.write('dir1/dir1/file0', '')
    topDir.write('dir1/dir1/file1', '1')
    topDir.write('dir1/dir1/file2', '22')
    topDir.write('dir1/dir2/file0', '')
    topDir.write('dir1/dir2/file1', '1')
    topDir.write('dir1/dir2/file2', '22')
    topDir.write('dir2/dir1/file0', '')
    topDir.write('dir2/dir1/file1', '1')
    topDir.write('dir2/dir1/file2', '22')
    topDir.write('dir2/dir2/file0', '')
    topDir.write('dir2/dir2/file1', '1')
    topDir.write('dir2/dir2/file2', '22')

"""
def fill_directory_tree2(topDir, depth):
    if depth > 9:
        raise ValueError('Depth must be 0 to 9')
    if depth == 0:
        return
    if depth > 0:
        write_files(topDir, depth)
    if depth > 1:
        subDirs = create_subdirs(topDir, depth)
        for subDir in subDirs:
            topDir.makedir(subDir)
            subPath = os.path.join(topDir, subDir)
            fill_directory_tree2(sub, depth-1)


def create_subdirs(topDir, depth):
    if depth <= 1:
        return
    return [''.join(['dir', str(i)]) for i in xrange(0, depth+1)]
"""


def create_valid_source_and_destination_paths(test_case_obj):
    test_case_obj.srcDir = TempDirectory()
    test_case_obj.destDir = TempDirectory()
    test_case_obj.extractDir = TempDirectory()
    test_case_obj.srcPath = test_case_obj.srcDir.path
    test_case_obj.archiveName = 'archive.tar'
    test_case_obj.archivePath = os.path.join(test_case_obj.destDir.path,
        test_case_obj.archiveName)
    test_case_obj.extractPath = test_case_obj.extractDir.path


def create_invalid_source_and_destination_paths(test_case_obj):
    test_case_obj.invalidDirParent = TempDirectory()
    test_case_obj.invalidPath = os.path.join(
        test_case_obj.invalidDirParent.path, 'thisDirDoesNotExist')
    test_case_obj.invalidSrcDir = test_case_obj.invalidPath
    test_case_obj.invalidArchivePath = os.path.join(test_case_obj.invalidPath,
        test_case_obj.archiveName)
    test_case_obj.invalidExtractPath = test_case_obj.invalidPath


def cleanup_temporary_directories(test_case_obj):
    test_case_obj.srcDir.cleanup()
    test_case_obj.destDir.cleanup()
    test_case_obj.invalidDirParent.cleanup()


def member_is_at_relative_path(member):
    return not os.path.isabs(member.name)
