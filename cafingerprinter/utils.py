
import os
import contextlib
import pygit2
import pathlib

def list_all_git_files(repopath):
    repo = pygit2.Repository(repopath)
    idx = repo.index
    idx.read()

    files = []
    for entry in idx:
        if os.path.isfile(entry.path):
            files.append(entry.path)

    return files

@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)

include_subexts = ['.min', '.manifest', '.config', '.tar']

def get_file_ext(filename):
    """
    Normal os.path.splitext does not think .min.js is a full extension
    This function combines select prior suffixes like .min
    """
    p = pathlib.Path(filename)
    if len(p.suffixes) <= 1:
        return p.suffix
    elif p.suffixes[-2] in include_subexts:
        return ''.join(p.suffixes[-2:])
    else:
        return p.suffix

def get_safe_file_ext(filename):
    return get_file_ext(filename).replace('.', '_')

class DotDict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
