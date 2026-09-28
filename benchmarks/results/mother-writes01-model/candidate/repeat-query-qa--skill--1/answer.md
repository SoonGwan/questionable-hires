I’ll use the mother-in-law skill to audit the submission sequences and retain deterministic component tests, leaving production code unchanged.


`Search.submit` uses query equality to decide which response is newest. That appears to let an older identical-query response overwrite the newer one. I’ll test this with separately controlled requests, alongside a different-query control, checking the complete displayed payload at each requested checkpoint.


Extended `test_search.py`, preserving the initial-state test and production files.

Ran `python3 -B -m unittest -v test_search`: **2 passed, 1 failed**.

- Different-query reverse completion: all complete-payload assertions passed.
- Identical-query reverse completion: retention after both submissions and newest completion passed. Older completion incorrectly replaced the newest payload with stale data.

The bug remains a failing regression. Tests verify actual fetch keys, control requests separately, bound waits to one second, and cancel/await owned tasks in `finally`.

Component QA only; no browser QA, network, sleeps, or scratch files.
