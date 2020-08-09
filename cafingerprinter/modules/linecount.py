"""
Example analysis module, just counts the number of lines in the file.
"""

import statistics

from .base import CafpModule

def _get_line_count(file):
    try:
        with open(file, 'r') as f:
            return sum(1 for line in f)
    except UnicodeDecodeError:
        log.err(f"File {file} is probably binary.")
        return None

class CafpLineCounter(CafpModule):
    def _run_file_analysis(self):
        return self._foreach_gitfile(_get_line_count)

    def _run_repo_analysis(self):
        return {
            "mean": statistics.mean([v for k,v in self.file_results.items()]),
        }
