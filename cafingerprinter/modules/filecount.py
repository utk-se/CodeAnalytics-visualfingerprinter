"""
Example analysis module, just counts the number of lines in the file.
"""

import statistics

from cadistributor import log
from .base import CafpModule

def _get_file_type(file):
    if '.' in file.split('/')[-1]:
        return file.split('.')[-1]

class CafpFileCounter(CafpModule):
    def _run_file_analysis(self):
        cnts = self._foreach_gitfile(_get_file_type)
        cnts = {k: v for k, v in cnts.items() if v is not None}
        return cnts

    def _run_repo_analysis(self):
        file_exts = [(k.split('.')[-1]) for k,v in self.file_results.items() if '.' in k.split('/')[-1]]
        result = {
            "sum": len(self.file_results),
            "by_ext": {k: 0 for k in file_exts}
        }
        for k, v in self.file_results.items():
            if k.split('.')[-1] in file_exts:
                result['by_ext'][k.split('.')[-1]] += 1

        return result
