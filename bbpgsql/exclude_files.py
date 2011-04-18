def exclude(tarinfo):
    excludes = ['exclude_this', 'exclude_this_too']
    for excluded_name in excludes:
        if tarinfo.name == excluded_name:
            return None
    return tarinfo
