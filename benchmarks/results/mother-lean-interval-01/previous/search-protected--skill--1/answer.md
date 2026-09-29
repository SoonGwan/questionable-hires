I’ll read the mother-in-law skill and inspect Search, then add and run a deterministic local test without changing production code.

Search uses a generation counter to decide which request may update the result. I’ll test both completion orders and check that an existing result stays visible while the newer request is pending, including after the older request finishes. There’s no existing test suite, so I’ll add a standalone standard-library test.

All 3 tests passed using actual `Search` with controlled futures. No stale-result defect reproduced.

- Older finishes first: existing result remains visible while newer is pending.
- Newer finishes first: late older completion cannot overwrite it.
- Existing result is retained when either request starts loading.

Kept rerunnable component tests in [test_search.py](project/test_search.py), with one-second bounded waits and owned-task cleanup. Production files and existing user changes were preserved.

Run:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search.py
```
