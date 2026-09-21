I’ll inspect `Loader.load` and the existing tests, update how callers share in-flight fetches, then add controlled cancellation tests and run the full unittest suite.

The current code lets a caller’s cancellation reach the shared fetch, and removes the in-flight entry whenever any caller exits. I’ve shielded the fetch and moved cleanup to its completion callback. The tests will check that late callers still join it after cancellations, and that an abandoned fetch’s failure is observed before retry.

Fixed `Loader.load` to shield shared fetches from caller cancellation, retain active fetches, observe abandoned failures, and clear completed fetches without caching. Result and error identity are preserved.

Added six controlled tests with bounded waits and owned cleanup; existing tests remain unchanged.

Verified: `python3 -B -m unittest discover -v` — all 7 tests pass.
