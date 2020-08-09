"""
Example analysis module, just counts the number of lines in the file.
"""

import statistics

from cadistributor import log
from .base import CafpModule

def _get_line_count(file):
    try:
        with open(file, 'r') as f:
            return sum(1 for line in f)
    except UnicodeDecodeError:
        log.warn(f"File {file} is probably binary.")
        return None

class CafpLineCounter(CafpModule):
    def _run_file_analysis(self):
        cnts = self._foreach_gitfile(_get_line_count)
        cnts = {k: v for k, v in cnts.items() if v is not None}
        return cnts

    def _run_repo_analysis(self):
        file_exts = [(k.split('.')[-1]) for k,v in self.file_results.items() if '.' in k.split('/')[-1]]
        raw_nums = [v for k,v in self.file_results.items()]
        result = {
            "sum": sum(raw_nums),
            "mean": statistics.mean(raw_nums),
            "by_ext": {}
        }
        for ext in file_exts:
            result['by_ext'][ext] = sum([v for k,v in self.file_results.items() if k.endswith('.'+ext)])
        return result
