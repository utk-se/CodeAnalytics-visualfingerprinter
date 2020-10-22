# CodeAnalytics Visual Fingerprinter

This code analysis program contains a number of modules that gather statistics about a git repo.

# Usage

`python setup.py install`

```
usage: ca-fingerprinter [-h] [--json results.json] [--quiet] [--perfile] [--skip module_name | --only module_name]
                        ./path/to/repo
```

# Modules

Each module is a standalone type of analysis that reports a small set of data about the repo being analyzed in a JSON-compatible format.

For example the `linecount` module counts total lines and total, average lines per file extension. The `indentation` module counts spaces and tabs at the beginning of lines. The `filecount` module just counts how many files there are and how many of each extension.

I think you get the idea, each one only does a specific small task, so to get the full 'fingerprint' we run all of the modules by default.
