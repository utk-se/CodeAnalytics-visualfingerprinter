"""
Per-file:
  Tabs or spaces
  TODO Find shiftwidth/tabstop by leading whitespace GCD
  TODO (other module?) Find mixed indent in files
  TODO (other module?) Find outlier indent (e.x. two-space indent in 4-space indent trending file)

Aggregation:
  Tabs vs spaces total usage
  TODO Outlier occurence frequency trends
"""

import re
import numpy as np

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

class CafpIndentationAnalyzer(CafpModule):
    def _build_line_indent_list(self):
        lines_files = self._foreach_gitfile()

    def _run_file_analysis(self):
        cnts = self._foreach_gitfile(_get_indentation_levels)
        results = {}
        for fname, ilevel in cnts.items():
            if ilevel is None:
                continue
            results[fname] = {}

            indent_type = ilevel.sum(axis=1)
            results[fname]["indent_type"] = indent_type.tolist()

            # results[fname]["spaces_raw"] = ilevel[0].tolist()
            # results[fname]["tabs_raw"] = ilevel[1].tolist()
        return results

    def _run_repo_analysis(self):
        # file_exts = [(k.split('.')[-1]) for k,v in self.file_results.items() if '.' in k.split('/')[-1]]
        t_spaces = sum([v["indent_type"][0] for k,v in self.file_results.items()])
        t_tabs   = sum([v["indent_type"][1] for k,v in self.file_results.items()])
        return {
            "totals": {
                "spaces": t_spaces,
                "tabs": t_tabs
            }
        }
