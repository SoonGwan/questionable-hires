I’ll inspect the search flow and local test setup, then test controlled request completion orders without changing production files.

`Search.run` uses a generation counter to decide whether a completed request may update the result. I’ll test both completion orders, check the result while the newer request is still pending, and verify that an existing result stays visible during loading.

No stale-result defect reproduced. All 3 deterministic tests passed:

- Older finishes first: ignored while newer remains pending; newer then displays.
- Newer finishes first: older completion cannot overwrite it.
- Existing result stays displayed during loading, including after older completion.

Tests use actual `Search`, controlled futures, bounded event/task waits, and owned-task cleanup. Production `search.py` is unchanged; SHA-256 verified.

Rerunnable test: [test_search_race.py](project/test_search_race.py)

```sh
python3 -B -m unittest -v test_search_race
```
