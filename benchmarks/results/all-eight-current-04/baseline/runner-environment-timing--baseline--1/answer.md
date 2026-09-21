I’ll inspect the worker, test setup, and incident command, then run local checks to pin down why the attempt counts differ. I won’t modify files.

The discrepancy is deterministic **import timing**, not an intermittent cache problem.

`worker.py:3` reads the environment once into `RETRIES`. `test_worker.py:4` imports the worker before `setUp()` runs. With the variable absent, `RETRIES` becomes `2`. Setting the environment to `'0'` afterward leaves that integer unchanged, so `range(RETRIES + 1)` makes three attempts.

Fresh Python processes using the actual worker and test setup produced:

| Scenario | Environment after `setUp` | `worker.RETRIES` | Attempts |
|---|---|---|---|
| Test, variable initially absent | `'0'` | `2` | 3; fails |
| Test, variable set before import | `'0'` | `0` | 1; passes |
| Incident standalone equivalent | Set before import | `0` | 1 |

The unmodified unittest also reproduced `AssertionError: 3 != 1`. Instrumentation confirmed `worker` was initially absent from `sys.modules`.

For the documented startup configuration behavior, set the environment before importing the worker; a delivery unit test can instead patch `worker.RETRIES`. Reading the environment inside `deliver()` would introduce live configuration behavior, which the incident does not require.

No files were changed; file hashes were verified unchanged. Runs used `-B` to disable bytecode writes, with no external services or dependencies.
