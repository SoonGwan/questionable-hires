I’ll inspect the search flow and local test setup, then test the actual `Search` with controlled request completions. I’ll keep a rerunnable test and leave production files unchanged.

`Search` uses a generation counter to prevent an older request from replacing a newer result. There are no existing tests or user changes. I’ll test both completion orders and check the displayed value while the newer request is still pending, including when a result is already displayed.

No stale-result defect reproduced. All 3 tests passed using actual `Search` with controlled futures:

- Newer finishes first: older completion does not overwrite it.
- Older finishes first: result stays `None` while newer remains pending, then displays the newer result.
- Existing result stays displayed during loading, including after older completion.

Kept `test_search_overlap.py` with bounded behavior-dependent waits and owned-task cleanup. Production `search.py` is unchanged, verified by hash and Git diff.

Rerun:
```sh
python3 -B -m unittest -v test_search_overlap
```
