I’ll compare `Preview.refresh` with the requirements, add controlled async tests, and run the requested unittest command.


`refresh` currently lets an older call clear `pending` while the latest call is unresolved. I’ll restrict that cleanup to the owning generation and test overlapping calls with manually settled futures.


All eight tests passed. They cover both completion orders, failure and cancellation ownership, retries, synchronous callback failure, object identity, retained display values, and instance isolation. I’ll check the final diff for unrelated changes and rerun the suite.


Fixed `preview.py`: only the latest-started refresh clears `pending`; overlapping calls remain allowed.

Added eight standard-library tests using actual `Preview`, controlled callbacks, bounded waits, task cleanup, and no timing sleeps. All requested cases are covered. Requirements and owner notes are unchanged.

Ran `python3 -B -m unittest discover -v` twice. Both native runs reported:

```text
Ran 8 tests in 0.043s

OK
```

Both test processes exited with code **0**.
