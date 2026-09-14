I’ll use the mother-in-law skill to test the actual Search with controlled request completions, keeping production code unchanged and leaving a rerunnable local test.

The project contains only `search.py`; there’s no existing test runner or separate product contract. Search uses a generation counter to guard result updates. I’ll test both completion orders and assert that a previously displayed result stays visible when the older request finishes while the newer one is still pending.

No stale-result defect reproduced. All 3 tests passed against actual `Search` using controlled futures.

- Normal request: displays its result.
- Older finishes while newer is pending: existing displayed result remains.
- Newer finishes first: its result survives the older completion.
- Existing result remains visible when overlapping requests start.

Saved [tests/test_search.py](project/tests/test_search.py), with one-second behavior-dependent waits and owned-task cleanup. Production files and existing user changes were preserved.

Rerun:
```sh
python3 -B -m unittest discover -s tests -v
```

Tested at the component layer, not rendered UI.
