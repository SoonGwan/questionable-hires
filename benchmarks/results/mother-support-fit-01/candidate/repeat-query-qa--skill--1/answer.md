I’ll read the mother-in-law skill and search requirements, then add controlled async regressions and run the requested unittest command. This will be component QA, not browser QA.

`Search.submit` uses the query text to identify the newest request, so overlapping identical queries appear able to overwrite each other. I’ll test both requested reverse-order sequences and add an identical-query case where the older response arrives while the newer request is still pending, to check payload retention throughout loading.

Extended `test_search.py`, preserving the initial-state test. Component QA only; no browser QA.

Ran `python3 -B -m unittest -v test_search`: **4 tests, 2 passed, 2 failed**.

- Different-query reverse order passed all complete-payload assertions.
- Identical-query reverse order failed: older completion replaced the newest payload.
- Identical-query older-first failed: older completion replaced the previous payload while newest remained pending.
- Initial-state test passed.

Tests check actual fetch keys, independently control responses, bound waits to one second, and cancel/await owned tasks in `finally`.

Failures remain ordinary regressions. Production and requirements are unchanged; no scratch files were created.
