"""
Example analysis module, just counts the number of lines in the file.
"""

import statistics
from multiprocessing import Pool

from cadistributor import log
from .base import CafpModule
from ..utils import get_file_ext

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
        file_exts = [get_file_ext(k) for k,v in self.file_results.items()]
        raw_nums = [v for k,v in self.file_results.items()]
        result = {
            "sum": sum(raw_nums),
            "mean": statistics.mean(raw_nums) if len(raw_nums) > 0 else 0,
            "by_ext": {k: 0 for k in file_exts},
            "mean_by_ext": {k: 0 for k in file_exts},
        }
        filecounts = {k: 0 for k in file_exts}
        for k, v in self.file_results.items():
            if get_file_ext(k) in file_exts:
                result['by_ext'][get_file_ext(k)] += v
                filecounts[get_file_ext(k)] += 1
        for k, v in filecounts.items():
            # print(f"{k}: {v}")
            result['mean_by_ext'][k] = result['by_ext'][k] / v

        return result
