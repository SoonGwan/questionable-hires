I’ll use the mother-in-law skill to audit submission ordering, add controlled async regressions, and run the requested unittest command. This is component QA; I won’t change production code or run browser QA.


The requirements give ownership to each submission, but `Search.submit` tracks only the query text. That appears to let an older identical-query response overwrite the newest result. I’ll test that sequence and a different-query control, checking the full structured payload at every requested checkpoint.


Extended `test_search.py`, preserving the initial-state test.

Ran `python3 -B -m unittest -v test_search`: **2 passed, 1 failed**.

- Different-query reversed completion passes.
- Identical-query reversed completion fails: the older response replaces the newest complete payload.
- Full-payload assertions after both submissions and newest completion pass.

Tests control each request separately, verify actual fetch keys, bound waits to one second, and cancel/await owned tasks in `finally`.

The bug remains a failing regression. Production files are unchanged; no scratch was created. This was component QA, not browser QA.
