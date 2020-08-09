
import pygit2

def list_all_git_files(repopath):
    repo = pygit2.Repository(repopath)
    idx = repo.index
    idx.read()

    files = []
    for entry in idx:
        files.append(entry.path)

    return files
