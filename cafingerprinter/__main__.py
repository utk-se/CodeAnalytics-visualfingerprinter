"""Analyzes the visual identity of code."""

import sys
import argparse
from cadistributor import log

def analyze(repopath):
    pass

def main():
    parser = argparse.ArgumentParser(description="CA-VisualFingerprinter")
    parser.add_argument('repopath', metavar='repo', type=str, help="Path to repo to analyze")
    parser.add_argument('--json', metavar='json_outfile', type=str, help="Path to write result json", required=False)
    args = parser.parse_args()

    log.info(f"Running analyzer on {args.repopath}")
    log.err(f"Not implemented.")

if __name__ == "__main__":
    main()
