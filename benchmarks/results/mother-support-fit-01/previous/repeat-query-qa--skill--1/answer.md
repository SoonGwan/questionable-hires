I’ll use the mother-in-law skill to audit the submission sequence and add controlled async regressions. I’ll keep production unchanged and report component QA results separately from browser coverage.

`Search.submit` uses the query text to identify the newest request, so two pending requests with identical queries can both update the display. I’ll add regressions with separate response futures for each fetch call, checking the complete payload at each checkpoint. The different-query case will serve as the normal control.

Extended `test_search.py`, preserving the initial-state test.

Ran `python3 -B -m unittest -v test_search`: **3 tests, 2 passed, 1 failed**.

- Different queries, reverse completion: passed.
- Identical queries: retention after both submissions and newest completion passed. Older completion incorrectly replaced the complete newest payload. Retained as a failing regression.

Tests check actual fetch keys, independently control responses, bound waits, and cancel/await owned tasks in `finally`.

Production unchanged; no scratch created. Component QA only; browser QA was not performed.
