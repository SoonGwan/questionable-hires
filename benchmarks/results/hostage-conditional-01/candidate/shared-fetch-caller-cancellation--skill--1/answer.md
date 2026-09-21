I’m using the hostage-negotiator skill to keep the fix focused. I’ll inspect the loader and existing tests, add controlled cancellation tests, and run the required native suite.

The current loader awaits the fetch directly and removes it when any caller exits. I’ll shield the shared fetch from caller cancellation and move cleanup to fetch completion, including observing failures after all callers have cancelled.

All six tests now pass. The abandoned-failure test also verifies that the fetch task is released without an unhandled-exception report; I fixed that test’s retained references to cancelled callers. I’m reviewing the final diff for scope and cleanup.

Fixed `Loader.load` to shield shared fetches from caller cancellation and clean up on fetch completion, observing failures even after every caller cancels.

Added five controlled tests covering cancellation, completion, failure/retry, identity, and independent keys, with bounded waits and owned cleanup. Existing test preserved.

`python3 -B -m unittest discover -v`: all 6 tests passed. No dependencies or commits added.
