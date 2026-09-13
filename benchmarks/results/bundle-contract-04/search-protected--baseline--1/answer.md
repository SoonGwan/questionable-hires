I’ll inspect Search and the local test setup, then add a rerunnable test with controlled request completion. I’ll leave production files unchanged and report the observed behavior.


Search uses a generation counter to decide which response may update the displayed result. I’ll test both completion orders, including the state after the older request finishes while the newer one is still pending, and verify that loading retains an existing result.


No stale-result defect reproduced. All 3 deterministic tests passed using actual `Search`, controlled futures, bounded waits, and owned-task cleanup.

- Older completes first: existing result remains while newer is pending; newer then displays.
- Newer completes first: its result remains after older completes.
- Loading retains the existing displayed result.

Production `search.py` is unchanged, verified by diff and SHA-256.

Rerunnable test: [test_search_local.py](project/test_search_local.py)

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search_local
```
