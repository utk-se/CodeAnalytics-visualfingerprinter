"""Analyzes the visual identity of code."""

import sys
import argparse
import json

from cadistributor import log
from . import modules as cafpmodules

def analyze(repopath, modules=None):
    if modules is None:
        modules = cafpmodules._all_modules

    return cafpmodules.run_modules(modules, repopath)

def main():
    parser = argparse.ArgumentParser(description="CA-VisualFingerprinter")
    parser.add_argument('repopath', metavar='repo', type=str, help="Path to repo to analyze")
    parser.add_argument('--json', metavar='json_outfile', type=str, help="Path to write result json")
    parser.add_argument('--quiet', '-q', action='store_true', help="Reduce logging verbosity and don't print output.")

    which_modules = parser.add_mutually_exclusive_group()
    which_modules.add_argument('--skip', metavar='skip_modules', action='append', help="Skip an analysis module by name")
    which_modules.add_argument('--only', metavar='only_modules', action='append', help="Only run specified analysis module(s)")
    args = parser.parse_args()

    log.info(f"Running analyzer on {args.repopath}")
    r = analyze(args.repopath)

    if 'json_outfile' not in args and not args.quiet:
        log.info(f"Analysis output:\n{json.dumps(r, indent=2, sort_keys=True)}")

if __name__ == "__main__":
    main()
