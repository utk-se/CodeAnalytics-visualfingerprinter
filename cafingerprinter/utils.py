
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

def get_file_ext(filename):
    """
    Normal os.path.splitext does not think .min.js is a full extension
    This function combines all the suffixes, and is safe to store in mongo
    """
    p = pathlib.Path(filename)
    if len(p.suffixes) > 1:
        return ''.join(p.suffixes)
    # if p.suffixes == ['.min', '.js']:
    return p.suffix

def get_safe_file_ext(filename):
    return get_file_ext(filename).replace('.', '_')
