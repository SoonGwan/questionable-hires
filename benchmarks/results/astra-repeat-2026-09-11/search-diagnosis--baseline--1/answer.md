I’ll inspect the search flow and run a local experiment to distinguish a cache issue from a request timing issue, without changing production code.

The cause is an asynchronous request race. In `search.py:5`, every completed request overwrites `self.result`, even if a newer query has already finished.

The local experiment used the actual search and transport functions with a controlled request stub containing no cache:

- Old response → new response: correct final results.
- New response → old response: older results overwrite newer results.

Added `experiment.py`; reproduce with `python3 -B experiment.py`. All assertions passed. Production files remain unchanged, verified by SHA-256 hashes. No external services were used.
