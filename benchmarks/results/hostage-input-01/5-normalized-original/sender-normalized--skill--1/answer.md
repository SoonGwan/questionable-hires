I’m using the hostage-negotiator skill to keep the fix focused. I’ll read the sender contract and existing tests, add the regressions, and run the documented unittest suite.

The fix belongs in a `finally` block so synchronous errors, asynchronous errors, and cancellation all clear `pending`. I’ll preserve normalization and result/error propagation, and use bounded task support for the regressions so failed assertions still clean up their tasks.

The regressions reproduced the bug: four tests failed because `pending` stayed true after failure or cancellation. The existing success test, normalization checks, and success/duplicate regression passed. I’ll now apply the `finally` fix and rerun the suite.

Fixed `Sender.send` with `try/finally` cleanup, preserving normalization, duplicate suppression, and result/error propagation.

Preserved existing assertions and added six regressions covering cleanup, cancellation, retries, independent instances, and normalized callback values. Added local support for bounded waits and task cleanup.

`python3 -B -m unittest discover -v`: **7 tests passed**. Before the fix, four regressions failed. Diff checks passed.

Validation covers cooperative asyncio callbacks only. Protected files and unrelated changes were preserved; no commits or scratch files.
