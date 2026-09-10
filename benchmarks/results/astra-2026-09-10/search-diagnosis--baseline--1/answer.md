I’ll inspect the search flow and run a local experiment to distinguish a cache issue from a request-ordering issue, without changing production code.

Each completed request overwrites the displayed result; there’s no check that it belongs to the latest query. The transport sends `Cache-Control: no-cache`. I’ll use a local, cache-free fake transport to control response order and test whether a late response can reproduce the symptom.

The cause is a response-order race. In `search.py:5`, every completed request overwrites `self.result`, even if a newer query has already completed.

The local, cache-free experiment passed:

- Old response finishes first → final result is the new query.
- Old response finishes last → final result is the old query.

This reproduces the symptom without caching or network access.

Re-run with `python3 -B diagnose_search.py`. Only the experiment file was added; production code is unchanged.
