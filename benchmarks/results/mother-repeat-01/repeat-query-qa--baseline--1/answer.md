I’ll inspect the requirements and existing tests, add controlled overlapping-request regressions, then run the specified unittest command. I’ll leave production code unchanged and report component QA findings separately from browser QA.

`Search.submit` identifies the newest request by query text. That appears to let an older same-query response overwrite the newer payload. I’ll test that case alongside a different-query control, using a separate future for each fetch response and seeding the displayed payload through a successful request.

Extended `test_search.py`, preserving the initial-state test.

Ran `python3 -B -m unittest -v test_search`: **3 tests, 2 passed, 1 failed**.

- Identical queries: older completion incorrectly overwrites the newest complete payload. Retained as a failing regression.
- Different queries: reversed completion order behaves correctly.
- Assertions verify actual fetch keys and complete payloads at every requested checkpoint. Each request is independently controlled; waits are bounded and tasks cleaned up in `finally`.

Production files remain unchanged. No network, sleeps, or scratch files. This was component QA; browser behavior was not tested.
