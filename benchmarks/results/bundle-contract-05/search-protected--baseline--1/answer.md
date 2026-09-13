I’ll inspect the search flow and local test setup, then add a rerunnable test with controlled request completions while preserving production files and existing changes.

`Search.run` uses a generation counter so only the latest-started request can update the result. I’ll test both completion orders with empty and pre-populated results, including the interval when the older request has finished but the newer one is still pending.

No stale-result defect reproduced. All four tests passed using actual `Search` with controlled futures.

- Both completion orders preserved the newest request’s result.
- Older completion while newer remained pending left the display unchanged.
- Existing results remained displayed while loading.

The test uses bounded, behavior-dependent waits and cleans up its owned tasks. Production `search.py` is unchanged, verified by SHA-256.

Rerunnable test: [test_search_local.py](project/test_search_local.py)

```sh
python3 -B -m unittest -v test_search_local.py
```
