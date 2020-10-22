"""
Example analysis module, just counts the number of lines in the file.
"""

import statistics
import os

from cadistributor import log
from .base import CafpModule
from ..utils import get_safe_file_ext

def _get_file_type(file):
    return get_safe_file_ext(file.split('/')[-1])

class CafpFileCounter(CafpModule):
    def _run_file_analysis(self):
        cnts = self._foreach_gitfile(_get_file_type)
        cnts = {k: v for k, v in cnts.items() if v is not None}
        return cnts

    def _run_repo_analysis(self):
        file_exts = [v for k, v in self.file_results.items()]
        result = {
            "sum": len(self.file_results),
            "by_ext": {k: 0 for k in file_exts}
        }
        for k, v in self.file_results.items():
            if v in file_exts:
                result['by_ext'][v] += 1

        return result
