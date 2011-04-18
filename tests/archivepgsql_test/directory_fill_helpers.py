def generate_filenames(number):
    if number < 1 or number > 10:
        raise ValueError('Number of files out of range.  1 to 10 is valid')
    return [''.join(['file', str(index)]) for index in xrange(0, number)]


def generate_file_contents(number):
    if number < 1 or number > 10:
        raise ValueError('Number of files out of range.  1 to 10 is valid')
    return [str(index) * index for index in xrange(0, number)]


def write_files(dir, files):
    for file in files:
        dir.write(file[0], file[1])


def create_files(dir, number):
    fileNames = generate_filenames(number)
    fileContents = generate_file_contents(number)
    write_files(dir, zip(fileNames, fileContents))

def generate_dirnames(number):
    if number < 1 or number > 10:
        raise ValueError('Number of files out of range.  1 to 10 is valid')
    return [''.join(['dir', str(index)]) for index in xrange(0, number)]

def create_directories(parent, number):
    dirNames = generate_dirnames(number)
    for name in dirNames:
        parent.makedir(name)
