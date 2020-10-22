"""
This module counts how many lines exist at a specific indentation level.
"""

import re
import numpy as np
from collections import Counter

from cadistributor import log
from .base import CafpModule

indentation_re = re.compile('^([ \t]+)')

def _get_indentation_levels(file):
    try:
        with open(file, 'r') as f:
            lines = list(f)
            a = np.zeros((2, len(lines)), dtype='int64')
            for idx, line in enumerate(lines):
                ws = indentation_re.match(line)
                if ws:
                    s = ws.group(0)
                    a[0,idx] = s.count(' ')
                    a[1,idx] = s.count('\t')
            return a
    except UnicodeDecodeError:
        log.warn(f"File {file} is probably binary.")
        return None

class CafpIndentationLevelCounter(CafpModule):
    def _build_line_indent_list(self):
        lines_files = self._foreach_gitfile()

    def _run_file_analysis(self):
        cnts = self._foreach_gitfile(_get_indentation_levels)
        results = {}
        self.tmp = {}
        for fname, ilevel in cnts.items():
            if ilevel is None:
                continue
            results[fname] = {}
            self.tmp[fname] = {}
            l_spaces = ilevel[0].tolist()
            l_tabs   = ilevel[1].tolist()
            self.tmp[fname]['c_spaces'] = Counter(l_spaces)
            self.tmp[fname]['c_tabs']   = Counter(l_tabs)
            results[fname]['spaces'] = dict(self.tmp[fname]['c_spaces'])
            results[fname]['tabs']   = dict(self.tmp[fname]['c_tabs'])
        return results

    def _run_repo_analysis(self):
        t_spaces = Counter()
        t_tabs = Counter()
        for k,v in self.tmp.items():
            t_spaces += v['c_spaces']
            t_tabs += v['c_tabs']
        return {
            "lines_by_indent_level": {
                "spaces": dict(t_spaces),
                "tabs": dict(t_tabs)
            }
        }
