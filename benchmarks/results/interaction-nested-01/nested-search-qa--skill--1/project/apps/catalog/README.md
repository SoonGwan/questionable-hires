# Catalog search

Run QA from this directory: `python3 -B ../../tools/check.py --timeout 3 -- python3 -B -m unittest discover -s qa -p 'test_*.py' -v`.
The process deadline covers tests and cleanup. The runner reports child failure separately from timeout; inspect its JSON output. Requirements are in requirements.md.
