I’ll inspect the search flow and run a local experiment to test the cache hypothesis, without changing production code.

The search code assigns every completed response to the same result field, with no check that it belongs to the latest query. The transport sends `Cache-Control: no-cache`, but that alone doesn’t establish whether caching is involved. I’ll use a cache-free fake transport and control response order to test whether an older request can overwrite a newer result.

The cause is a response-order race in `Search.run`: every completed request overwrites `self.result`, even if a newer query has already returned.

Added a deterministic, cache-free experiment in `test_search_race.py`:

- Responses finishing in query order leave the newer result.
- An older response finishing last overwrites the newer result, reproducing the bug without caching.

Both checks passed with `python3 -B -m unittest -v test_search_race.py`. They confirm the diagnosis, not a fix. Production code is unchanged.
