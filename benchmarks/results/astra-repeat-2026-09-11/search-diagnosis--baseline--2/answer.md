I’ll inspect the search flow and run a local experiment to test the cache theory, without changing production code.


Each completed request writes directly to the shared result, with no check that it belongs to the latest query. I’ll control the completion order of two overlapping requests through a local transport stub to test whether an older response can overwrite the newer one without any cache involved.


The cause is a request-order race in `search.py`: every response overwrites `self.result`, even if a newer query has already completed.

The local, cache-free experiment confirmed:

- Old response finishes first → final result is the new query.
- Old response finishes last → it overwrites the new query’s result.

Both requests used the existing transport and its `Cache-Control: no-cache` header. No cache was needed to reproduce the bug.

Saved the reproducible experiment in `experiment_search_order.py`. Run with `python3 experiment_search_order.py`; all assertions passed. Production code is unchanged.
