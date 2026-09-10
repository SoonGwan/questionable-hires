I’ll inspect the search flow and run a local experiment to test the cache hypothesis, without changing production code.

`Search.run` assigns every completed response to the same result field, with no check for a newer query. The transport sends `Cache-Control: no-cache`, but that alone doesn’t rule out caching. I’ll use a cache-free fake request and control completion order to test whether an older response can overwrite the newer result.

The cause is a response-order race: `Search.run` writes every response to `self.result`, even when a newer query has already completed.

Added [test_search_race.py](project/test_search_race.py), a deterministic, cache-free local experiment:
- Older response first → newer results remain.
- Newer response first → older results overwrite them.

Both checks passed, reproducing the bug without a cache. Production code is unchanged.

Verify with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search_race`.
