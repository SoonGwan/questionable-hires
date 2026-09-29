I’ll read the exorcist skill and trace the worker’s test setup, then run local experiments without changing any files.

The worker reads `REQUEST_RETRIES` at import time, and the test imports it before `setUp` patches the environment. I’ll use the existing unittest to record the effective retry count and callback calls, then compare fresh processes with the variable absent versus set before import.

The discrepancy is deterministic **import timing**. No intermittent cache problem is needed to reproduce it.

`worker.py:3` reads the environment once into `RETRIES`. `test_worker.py:4` imports the worker before `setUp` changes the environment. `deliver()` then uses that already assigned value.

Fresh-process experiments using the actual test, its original `setUp`, and the actual worker produced:

| Scenario | Environment after `setUp` | `worker.RETRIES` | Callback calls |
|---|---|---|---|
| Variable absent before import | `'0'` | `2` | 3; test fails |
| Variable set to `0` before import | `'0'` | `0` | 1; test passes |
| Incident’s standalone sequence | `'0'` | `0` | 1 |

The recording wrapper forwarded every call to the test’s original callback; it did not replace retry behavior. The uninstrumented test also failed with `AssertionError: 3 != 1`.

The distinguishing unittest commands are:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

`patch.dict` changes the environment, and `addCleanup` correctly restores it. Neither re-evaluates `worker.RETRIES`.

Given the documented startup configuration behavior, the test must arrange configuration before import or patch the effective worker setting when testing retry behavior. Whether production should support live configuration changes remains unspecified.

No files were changed, dependencies installed, or external services accessed. Python ran with `-B` to prevent bytecode writes.
