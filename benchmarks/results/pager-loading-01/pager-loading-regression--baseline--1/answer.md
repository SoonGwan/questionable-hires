I’ll read the existing tests and support code, add the three regression cases, then run the four-test native suite once. Production code will remain unchanged.

`Pager.select` clears loading unconditionally when any request finishes. I’ll assert the full state after each older request completes while the newer response is still pending, then let the newer request finish and check its result. The retry case will also check error clearing at entry and row retention.

Extended only `test_pager.py`; preserved the existing single-success test.

Ran `python3 -m unittest -v test_pager` once. Results under `test_pager.PagerTests`:

- `test_single_success`: PASS
- `test_older_success_while_newer_pending`: FAIL
- `test_older_oserror_while_newer_pending`: FAIL
- `test_latest_error_followed_by_successful_retry`: PASS

Both failures demonstrate that older completion clears `loading` while the newer request remains pending. Rows and error remain correct; newer success checks also pass.

Tested native asynchronous `Pager.select` behavior with deterministic responses, bounded waits and fixture-owned cleanup. Production unchanged; regression failures retained.
