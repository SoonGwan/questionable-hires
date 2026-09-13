I’ll inspect the search flow and local test setup, then use controlled futures to check both completion orders without changing production files.

`Search.run` uses a generation counter to reject results from superseded requests. I’ll test the actual class with controlled futures in both completion orders, including checks that an existing result stays visible while loading and that an older completion cannot replace it while the newer request is pending.

No stale-result defect reproduced. Both deterministic tests passed using actual `Search` with controlled futures.

- Older finishes first: existing result remains while newer is pending; newer then displays.
- Newer finishes first: newer displays; older completion cannot overwrite it.
- Existing result stays visible while requests load.

Retained [test_search_overlap.py](project/test_search_overlap.py), with bounded behavior-dependent waits and owned-task cleanup. Production `search.py` is unchanged, verified by SHA-256 and Git diff.

Rerun:
```sh
python3 -B -m unittest -v test_search_overlap.py
```
