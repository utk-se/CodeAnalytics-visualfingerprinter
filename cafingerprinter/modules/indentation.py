"""
Per-file:
  Tabs or spaces
  Find shiftwidth/tabstop by leading whitespace GCD
  Find mixed indent
  Find outlier indent (e.x. two-space indent in 4-space indent trending file)

Aggregation:
  Outlier occurence frequency trends
"""

from .base import CafpModule

class CafpIndentationAnalyzer(CafpModule):
    def _build_line_indent_list(self):
        lines_files = self._foreach_gitfile()
