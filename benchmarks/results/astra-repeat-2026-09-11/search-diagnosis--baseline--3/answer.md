I’ll inspect the search flow and run a local experiment to test the cache theory, without changing production code.

`Search.run` assigns every completed response to the same result field, without checking which query is newest. I’ll test both response orders through the local transport using a cache-free fake request to see whether a late response can reproduce the symptom.

The cause is an out-of-order response race. In `search.py:5`, every completed request overwrites `self.result`, even if a newer query has already finished.

The local experiment used the existing transport with a cache-free fake request:

- Old response finishes first → final result is **new**.
- New response finishes first → late old response overwrites it; final result is **old**.

This reproduces the symptom without caching.

Saved the reproducible experiment in `experiment_search_race.py`. Run with `python3 -B experiment_search_race.py`; all assertions passed. Production code is unchanged.
