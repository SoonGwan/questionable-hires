I’m using the hostage-negotiator skill to review the refresh contract, keep any fix focused, and add controlled async tests with bounded waits and cleanup.



`Preview.refresh` already publishes only the latest result, but every call clears `pending` in `finally`. An older call can therefore clear it while the latest is still running. I’ll guard that cleanup by generation and test the completion, failure, cancellation, and retry paths.



The fix and eight tests are in place. The tests use the actual `Preview` with controlled callbacks, check result and exception identity, and cancel and drain owned tasks during cleanup. I’ll now run the requested unittest command and check the final diff and helper-copy integrity.



Fixed `Preview.refresh` so only the latest-started call clears `pending`; overlapping calls remain allowed.

Added eight standard-library tests covering all requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Actual run: `python3 -B -m unittest discover -v` reported **8 tests, all OK**. Test process exit: **0**. Helper integrity and diff checks also passed.
