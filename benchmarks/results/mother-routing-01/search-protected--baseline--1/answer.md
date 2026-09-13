I’ll inspect the search flow and local test setup, then test request ordering with controlled futures without changing production code.

`Search.run` uses a generation counter to prevent an older request from replacing a newer result. I’ll test both completion orders with both an empty result and an existing displayed result, including the point where the older request finishes while the newer one is still pending.

No stale-result defect reproduced. All 4 deterministic tests passed using actual `Search` and controlled futures.

- Both completion orders preserve the newer result.
- Older completion while newer remains pending leaves the displayed result unchanged.
- An existing result remains displayed while loading.

Tests use bounded event/task waits and owned-task cleanup. `search.py` is unchanged; SHA-256 verified.

Saved rerunnable tests in [test_search_overlap.py](project/test_search_overlap.py).

```sh
python3 -B -m unittest -v test_search_overlap
```
