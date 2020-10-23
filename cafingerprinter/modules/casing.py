"""
https://en.wikipedia.org/wiki/Naming_convention_(programming)

Per-file:
  Dominant and outlier casing styles for:
    variables
    functions
    classes

Aggregation:
  aggregated casing style (dominant, outlier) for each naming type
"""

from enum import Enum
from collections import Counter
from functools import lru_cache

from cadistributor import log
from .base import CafpModule
from ..utils import get_safe_file_ext as get_file_ext
from ..lexing.pygments_proxy import token, get_tokens_for_file

# https://stackoverflow.com/a/51976841/2375851
class CasingScheme(str, Enum):
    other = "other"
    invalid = "invalid"
    camel = "CamelCase"
    lowercamel = "lowerCamelCase"
    snake = "snake_case"
    tallsnake = "TALL_SNAKE_CASE"
    kebab = "kebab-case"
    tallkebab = "KEBAB-CASE"
    flat = "flatcase"
    upper = "UPPERCASE"

# (has_upper, has_lower, has_dash, has_underscore, first_upper)
_case_id_map = {
    (True,  True,  False, False, True  ): CasingScheme.camel,
    (True,  True,  False, False, False ): CasingScheme.lowercamel,
    (False, True,  False, True,  False ): CasingScheme.snake,
    (True,  False, False, True,  True  ): CasingScheme.tallsnake,
    (False, True,  True,  False, False ): CasingScheme.kebab,
    (True,  False, True,  False, True  ): CasingScheme.tallkebab,
    (False, True,  False, False, False ): CasingScheme.flat,
    (True,  False, False, False, False ): CasingScheme.upper,
    (False, False, False, False, False ): CasingScheme.invalid,
}

## Why use a cache here?
# Files are very likely to contain the same name many times, and these string
# operations are relatively expensive to identify the casing of the name.
## Why this maxsize?
# no idea, just a random guess
# but it works: CacheInfo(hits=4466185, misses=693405, maxsize=4000, currsize=4000
# 4.4 million vs 0.7 million
@lru_cache(maxsize=4000)
def classify_casing_scheme(token_text):
    """Given a string, return the casing type"""
    if not token_text.isprintable():
        return CasingScheme.invalid
    has_upper = not token_text.islower()
    has_lower = not token_text.isupper()
    has_dash = '-' in token_text
    has_underscore = '_' in token_text
    first_upper = token_text[0].isupper() if len(token_text) > 0 else False
    case_id = (has_upper, has_lower, has_dash, has_underscore, first_upper)
    if case_id in _case_id_map:
        return _case_id_map[case_id]
    return CasingScheme.other

# https://pygments.org/docs/tokens/#module-pygments.token
target_token_types = [
    token.Name,
]
# subtypes of target_token_types we want to exclude
exclude_token_types = [
    token.Name.Function.Magic,
    token.Name.Variable.Magic,
    token.Name.Entity, # (e.g. &nbsp; in HTML)
    token.Name.Builtin,
]

def _is_token_targetable(tokentype):
    if tokentype in exclude_token_types:
        return False
    if tokentype in target_token_types:
        return True
    for exclude_type in exclude_token_types:
        if tokentype in exclude_type:
            return False
    for target_type in target_token_types:
        if tokentype in target_type:
            return True
    return False

# reducing within the _foreach_gitfile step to avoid massive memory requirements
# the size of tokens for a file is multiples larger than the file itself
def _tokenize_and_reduce_file(filename):
    raw_tokens = get_tokens_for_file(filename)
    if raw_tokens is None:
        # log.debug(f"File {filename} failed to lex.")
        return None
    target_tokens = []
    for (idx, tokentype, value) in raw_tokens:
        if _is_token_targetable(tokentype):
            target_tokens.append((idx, tokentype, value))
    return target_tokens

class CafpCasingAnalyzer(CafpModule):
    def _run_file_analysis(self):
        tokenized = self._foreach_gitfile(_tokenize_and_reduce_file)
        # ignore non-lexable files:
        for k in list(tokenized.keys()):
            if tokenized[k] is None:
                del tokenized[k]

        casings = {}
        self.tmp.counters = {}
        for filename, tokens in tokenized.items():
            casings[filename] = {}
            self.tmp.counters[filename] = {}
            tokens_with_cases = []
            for (idx, tokentype, value) in tokens:
                case = classify_casing_scheme(value)
                tokens_with_cases.append((tokentype, case))
            self.tmp.counters[filename] = Counter(tokens_with_cases)
            for (tokentype,casing),v in self.tmp.counters[filename].items():
                tokenname = str(tokentype)
                # log.debug(f"{filename} {(tokentype,)}/{tokenname} with {casing}")
                if tokenname not in casings[filename]:
                    casings[filename][tokenname] = {}
                if casing.name not in casings[filename][tokenname]:
                    casings[filename][tokenname][casing.name] = 0
                casings[filename][tokenname][casing.name] += v
            # casings[filename] = {str(k): v for k,v in dict(self.tmp.counters[filename]).items()}
        return casings

    def _run_repo_analysis(self):
        by_ext = {}
        total = {}
        for f_k, f_v in self.file_results.items():
            f_ext = get_file_ext(f_k)
            if f_ext not in by_ext:
                by_ext[f_ext] = {}
            for tokentype,casecounts in f_v.items():
                if tokentype not in total:
                    total[tokentype] = {}
                for casing,count in casecounts.items():
                    if casing not in total[tokentype]:
                        total[tokentype][casing] = 0
                    total[tokentype][casing] += count
                    if tokentype not in by_ext[f_ext]:
                        by_ext[f_ext][tokentype] = {}
                    if casing not in by_ext[f_ext][tokentype]:
                        by_ext[f_ext][tokentype][casing] = 0
                    by_ext[f_ext][tokentype][casing] += count
        return {
            "total": total,
            "by_ext": by_ext,
        }

    def exit_cleanup(self):
        log.debug(f"classify_casing_scheme cache: {classify_casing_scheme.cache_info()}")
