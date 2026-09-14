I’ll inspect the search flow and local test setup, then add a rerunnable test with controlled futures. I’ll leave production files unchanged and check each requested completion and loading state.

`Search` checks a generation counter before displaying a result, which appears to prevent an older request from overwriting a newer one. I’ll test both completion orders on the actual class, including whether an existing result stays visible while requests are pending.

No stale-result defect reproduced. Both tests passed using actual `Search` with controlled futures:

- Older finishes first: existing result remains displayed while newer is pending; newer then replaces it.
- Newer finishes first: its result remains displayed after older finishes.
- Existing results remain visible while loading.

Tests use bounded, completion-dependent waits and clean up owned tasks. Production `search.py` is unchanged, verified by SHA-256.

Rerunnable test: [test_search_overlap.py](project/test_search_overlap.py).

```sh
python3 -B -m unittest -v test_search_overlap
```
