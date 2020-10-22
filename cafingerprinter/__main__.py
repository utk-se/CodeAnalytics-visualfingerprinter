"""Analyzes the visual identity of code."""

import os
import sys
import argparse
import json
from bson.json_util import dumps, loads

from cadistributor import log
from . import utils
from . import modules as cafpmodules

def analyze(repopath, modules=None, per_file_results=False):
    _m_classes = []
    if modules is None:
        _m_classes = cafpmodules._all_modules
    else:
        for m in modules:
            try:
                _m_classes.append(cafpmodules._class_by_name[m])
            except KeyError as e:
                log.error(f"Could not find module {m}")
                log.error(e)
                raise
    log.debug(f"Modules: {_m_classes}")

    abspath = os.path.abspath(repopath)
    log.debug(f"Repo path {abspath}")
    with utils.pushd(abspath):
        return cafpmodules.run_modules(_m_classes, abspath, per_file_results)

def main():
    parser = argparse.ArgumentParser(description="CA-VisualFingerprinter")
    parser.add_argument('repopath', metavar='./path/to/repo', type=str, help="Path to repo to analyze")
    parser.add_argument('--json', metavar='results.json', type=str, help="Path to write result json")
    parser.add_argument('--quiet', '-q', action='store_true', help="Reduce logging verbosity and don't print the result.")
    parser.add_argument('--verbose', '-v', action='store_true', help="Enable debug logging.")
    parser.add_argument('--perfile', dest='per_file_results', action='store_true', help="Include per-file results in output json.")

    which_modules = parser.add_mutually_exclusive_group()
    which_modules.add_argument('--skip', metavar='module_name', dest='skip_modules', action='append', help="Skip an analysis module by name")
    which_modules.add_argument('--only', metavar='module_name', dest='only_modules', action='append', help="Only run specified analysis module(s)")
    args = parser.parse_args()

    if args.quiet:
        log.setLevel(log.WARN)
    if args.verbose:
        log.setLevel(log.DEBUG)
        log.debug("Debug output enabled.")

    modules = cafpmodules._friendly_names.values()
    if args.skip_modules:
        for m in args.skip_modules:
            log.info(f"Skipping module {m}")
            if m in modules:
                modules.remove(m)
    elif args.only_modules:
        modules = args.only_modules

    log.info(f"Running analyzer on {args.repopath}")
    r = analyze(args.repopath, modules, per_file_results=args.per_file_results)

    if not args.quiet:
        log.info(f"Analysis output:\n{json.dumps(r, indent=2, sort_keys=True)}")

    if 'json_outfile' in args:
        with open(args.json_outfile, 'w') as f:
            f.write(json.dumps)

    r_bson = dumps(r)
    log.info(f"Result BSON size: {len(r_bson)}")

if __name__ == "__main__":
    main()
