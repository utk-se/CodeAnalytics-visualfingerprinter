
import os
import contextlib
import pygit2

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
