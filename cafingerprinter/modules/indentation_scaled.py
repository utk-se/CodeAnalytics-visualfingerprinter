"""
For each file, compute indentation. Additionally 
"""

import statistics
from multiprocessing import Pool

from cadistributor import log
from .base import CafpModule
from scipy import interpolate

def line_start(line):
    return len(line) - len(line.lstrip())

def line_end(line):
    return len(line.rstrip())

def _get_indentation(file):
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            return {
                'indent_start': [len(line) - len(line.lstrip()) for line in lines],
                'line_end': [len(line.rstrip()) for line in lines]
            }
    except UnicodeDecodeError:
        log.warn(f"File {file} is probably binary.")
        return None


class CafpLineCounter(CafpModule):
    def _run_file_analysis(self):
        # TODO: proper passing of resolution
        heatmap_resolution = 100

        rv = self._foreach_gitfile(_get_indentation)

        # vertically (line wise) scale data to meet target resolution
        line_numbers_2d = [len(indent_dict['indent_start']) for indent_dict in rv.values()]
        indentation_idx = [indent_dict['indent_start'] for indent_dict in rv.values()]

        # interpolate vertically within a file
        interpolated_vec = []
        for n_lines, indentation_idx_vec in zip(line_numbers_2d, indentation_idx):
            interp = interpolate.interp1d(range(n_lines), indentation_idx_vec)
            interpolated_vec.append(interp(range(heatmap_resolution)))

        return interpolated_vec

    def _run_repo_analysis(self):
        # key of file results is file name
        file_exts = [(k.split('.')[-1]) for k,v in self.file_results.items() if '.' in k.split('/')[-1]]

        # track average and mode of the interpolated indentation points 

        
        for k, v in self.file_results.items():
            # TODO: FIX ME
            if k.split('.')[-1] in file_exts:
                result['by_ext'][k.split('.')[-1]] += v

        return result
