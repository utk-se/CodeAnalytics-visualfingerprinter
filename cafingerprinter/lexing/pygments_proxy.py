
import pygments
import pygments.lexers
import pathlib

from pygments import token
from cadistributor import log

def get_tokens_for_file(filepath):
    """Get the list of tokens for the file.

    If there is no Pygments lexer for the file extension then returns `None`

    We cannot / shall never use a cache here so that we can be 'pure' for
    the module _foreach_gitfile function to work without a data race.
    Performance sacrifice is not a primary concern.
    Also the memory footprint of a cache is impractical for large repos.
    Any cache that isn't cross-process is even more useless since most modules
    only get the result for one file once.
    """
    path = pathlib.Path(filepath)
    try:
        lxr = pygments.lexers.get_lexer_for_filename(path.name)
    except pygments.util.ClassNotFound as e:
        log.debug(f"{e}")
        return None
    with path.open('r') as f:
        log.debug(f"lexer tokenizing {path.name} ...")
        try:
            return lxr.get_tokens_unprocessed(f.read())
        except UnicodeDecodeError as e:
            log.warn(f"Lexer failed to decode {filepath}")
            return None
