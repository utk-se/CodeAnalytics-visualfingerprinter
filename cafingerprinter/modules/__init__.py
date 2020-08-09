
from .indentation import CafpIndentationAnalyzer as Indentation
from .casing import CafpCasingAnalyzer as Casing
from .linecount import CafpLineCounter as LineCount

_all_modules = [
    Indentation,
    Casing,
    LineCount,
]

# used for e.x. --skip=indentation or --only=casing,indentation
_friendly_names = {
    Indentation: "indentation",
    Casing: "casing",
    LineCount: "linecount",
}
_class_by_name = {v: k for k, v in _friendly_names.items()}

def run_modules(modulelist, repopath):
    insts = []
    for m in modulelist:
        insts.append(m(repopath))

    def get_module_results(i):
        i.run()
        return (i, i.file_results, i.repo_results)

    # TODO parallelism (requires kept order)
    results = list(map(get_module_results, insts))

    return {
        "file": dict(
            [(_friendly_names[x[0].__class__], x[1]) for x in results]
        ),
        "repo": dict(
            [(_friendly_names[x[0].__class__], x[2]) for x in results]
        ),
    }
