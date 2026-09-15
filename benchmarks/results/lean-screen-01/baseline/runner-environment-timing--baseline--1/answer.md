I’ll inspect the worker and test setup, then run local checks to trace where the retry count comes from.

**The discrepancy is deterministic import timing, not an intermittent cache problem.**

`worker.py:3` reads the environment once, when imported. `test_worker.py:4` imports it **before `setUp` runs**, so `worker.RETRIES` becomes the default `2`. Changing the environment in `setUp` does not update that variable. `range(RETRIES + 1)` therefore produces three attempts.

Local evidence using the actual worker and test setup:

| Scenario | Environment | `worker.RETRIES` | Attempts |
|---|---|---:|---:|
| Fresh test-module import | Absent | 2 | — |
| After actual `setUp()` | `"0"` | 2 | 3 |
| Standalone, zero set before import | `"0"` | 0 | 1 |

The actual unittest failed with `AssertionError: 3 != 1` when the variable was absent at startup, and passed when it was zero before import. Both ran in fresh Python processes with bytecode writing disabled.

Given the documented startup configuration behavior, the test should establish the environment before importing the worker, or patch `worker.RETRIES` when testing delivery behavior. Reading configuration on every call would be a separate behavior change.

No files were modified, dependencies installed, or external services accessed.
