
# from multiprocessing import Pool
from multiprocessing.pool import ThreadPool as Pool

from cadistributor import log
from .. import utils

class CafpModule():
    def __init__(self, repodir):
        self.repodir = repodir

    def _foreach_gitfile(self, function):
        """
        NOTE: function must be pure (excepting of course, debugging and file reading)

        arg function(file: str) -> json-compatible output
        output dict(filename: function_result)
        """
        files = utils.list_all_git_files(self.repodir)

        results = None
        with Pool() as pool:
            func_out = pool.imap(function, files)
            results = dict(zip(
                files,
                list(func_out)
            ))

        return results

    def start(self):
        """Returns started thread object
        """
        pass

    def _run_file_analysis(self):
        log.warn("Override me!")

    def _run_repo_analysis(self):
        log.warn("Override me!")

    def run(self):
        self.tmp = utils.DotDict()
        self.file_results = self._run_file_analysis()
        self.repo_results = self._run_repo_analysis()
        del self.tmp
