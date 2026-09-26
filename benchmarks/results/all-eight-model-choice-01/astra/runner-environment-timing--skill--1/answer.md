I’ll use the exorcist skill to compare the worker’s effective retry setting with the test setup, using local, deterministic evidence and leaving existing files unchanged.

The worker reads `REQUEST_RETRIES` at import time, and the test imports it before `setUp` runs. I’ll run the actual test with the variable absent and with it set before startup, and capture the environment value and effective retry count after `setUp`.

The discrepancy is deterministic **import-time configuration**.

[worker.py](project/worker.py#L3) reads the environment once. The test imports `worker` before `setUp`, so changing the environment afterward leaves `worker.RETRIES` at `2`: one initial attempt plus two retries.

Local evidence using the actual unittest and callback:

| Experiment | Result |
|---|---|
| `env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker` | Fails: `3 != 1` |
| `REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker` | Passes |
| Trace of actual test after `setUp` | Environment is `'0'`; `worker.RETRIES` remains `2`; callback runs three times |
| Incident’s standalone setup, setting zero before import | `worker.RETRIES=0`; callback runs once |

The fixture’s environment patch works, and cleanup restores it. Neither updates the already initialized module constant.

No intermittent cache behavior is needed to explain this reproduction. Startup configuration matches the documented application behavior; whether live changes should work remains unspecified.

No files were changed, dependencies installed, or external services accessed.
