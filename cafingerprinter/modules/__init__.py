
from multiprocessing import Pool
# from multiprocessing.pool import ThreadPool as Pool

from .indentation import CafpIndentationAnalyzer as Indentation
from .indentation_levelcounter import CafpIndentationLevelCounter as IndentationLevelCounter
from .casing import CafpCasingAnalyzer as Casing
from .linecount import CafpLineCounter as LineCount
from .filecount import CafpFileCounter as FileCount

# used for e.x. --skip=indentation or --only=casing,indentation
_friendly_names = {
    Indentation: "indentation",
    Casing: "casing",
    LineCount: "linecount",
    FileCount: "filecount",
    IndentationLevelCounter: "indentlevelcounter",
}
_class_by_name = {v: k for k, v in _friendly_names.items()}
_all_modules = _friendly_names.keys()

def get_module_results(i):
    i.run()
    return (i, i.file_results, i.repo_results)

def run_modules(modulelist, repopath, per_file_results=False):
    insts = []
    for m in modulelist:
        insts.append(m(repopath))

    results = []
    with Pool() as pool:
        results = pool.map(get_module_results, insts)
    # results = list(map(get_module_results, insts))

    if per_file_results:
        return {
            "files": dict(
                [(_friendly_names[x[0].__class__], x[1]) for x in results]
            ),
            "repo": dict(
                [(_friendly_names[x[0].__class__], x[2]) for x in results]
            ),
        }
    else:
        return {
            "repo": dict(
                [(_friendly_names[x[0].__class__], x[2]) for x in results]
            ),
        }
