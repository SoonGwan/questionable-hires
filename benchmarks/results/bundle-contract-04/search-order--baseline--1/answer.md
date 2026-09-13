I’ll inspect the search flow and local test setup, then add a rerunnable test with controlled overlapping requests. I’ll preserve production files and existing user changes.

`Search.run` assigns each response directly to the displayed result. If an older request finishes last, it appears able to overwrite the latest query’s result. I’ll test both completion orders using gated responses, with assertions that both requests overlap and bounded waits for each step.

The normal-order test passed. The reversed-order test reproduced the bug: `"cat"` results appeared first, then the older `"ca"` response replaced them. The saved output includes the overlap controls and exact failing assertion. Both tests bound their waits and clean up owned tasks.

Reproduced a stale-result bug against actual `Search`:

- Normal completion: **passes**.
- Reversed completion: **fails**—older `"ca"` results overwrite newer `"cat"` results.

Added `qa/test_search_overlap.py`. It controls overlapping requests, asserts intermediate states, bounds waits, and cleans up owned tasks. Exact assertions and controls are captured in `qa/search-overlap-results.txt`.

Rerun:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s qa -v
```

Expected current result: **1 pass, 1 failure**. Production files are unchanged, verified by hashes and Git diff.
