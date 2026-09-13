I’ll inspect the search flow and local test setup, then add a deterministic test using controlled futures without changing production code.

`Search` uses a generation counter to decide whether a completed request may update the result. I’ll test both completion orders, check the display after the older request finishes while the newer one is pending, and verify that loading retains an existing result.

No stale-result defect reproduced. All 3 deterministic tests passed:

- Newer finishes first: older completion cannot overwrite it.
- Older finishes first: existing result remains while newer is pending; newer then replaces it.
- Loading retains the existing displayed result.

Saved [test_search_local.py](project/test_search_local.py), using actual `Search`, controlled futures, bounded event/task waits, and owned-task cleanup.

Rerun: `python3 -B -m unittest -v test_search_local`

Production `search.py` is unchanged, verified by SHA-256 and Git diff.
