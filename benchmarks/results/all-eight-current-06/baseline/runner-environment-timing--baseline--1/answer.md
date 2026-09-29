I’ll inspect the worker, test setup, and incident command, then run local checks without changing any files.

The discrepancy is deterministic **import timing**, not an intermittent cache problem.

`worker.py:3` reads `REQUEST_RETRIES` once, when imported. `test_worker.py:4` imports it before `setUp()` patches the environment.

Local evidence using the actual worker and test:

| Check | Result |
|---|---|
| Fresh unittest process, variable absent | Fails: `3 != 1` |
| After importing the test module | Environment absent; `worker.RETRIES == 2` |
| After calling the actual `setUp()` | Environment is `'0'`; `worker.RETRIES` remains `2` |
| Standalone process with `REQUEST_RETRIES=0` before import | One attempt |
| Actual unittest with `REQUEST_RETRIES=0` before import | Passes |

`deliver()` runs `range(RETRIES + 1)`, so the stored value `2` produces three attempts. Patching the environment afterward does not recompute that value.

Given the documented startup configuration behavior, tests should set the environment before importing the worker—preferably in a fresh process—or patch `worker.RETRIES` when testing delivery logic. Reading the environment inside `deliver()` would introduce live configuration behavior that the incident does not require.

No files were changed, bytecode writes were disabled, and no external services were accessed.
