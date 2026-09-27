I’ll use the exorcist skill to compare the actual test and standalone setup, then run a deterministic local probe without changing existing files.

The worker reads `REQUEST_RETRIES` at import time, before the test’s `setUp` runs. I’ll run the actual test in fresh processes with the variable absent and set to zero, recording the effective retry value and callback count, then check the standalone case.

The discrepancy is deterministic import timing; no intermittent cache problem is needed to explain it.

[test_worker.py:4](project/test_worker.py) imports the worker before `setUp`. At import, [worker.py:3](project/worker.py) reads the environment once, defaulting `RETRIES` to `2`. Changing the environment afterward does not update that constant.

Fresh-process probes using the actual test and a recording callback showed:

| Startup environment | Environment after `setUp` | Effective retries | Attempts | Result |
|---|---|---:|---:|---|
| Variable absent | `0` | 2 | 3 | Test fails |
| `REQUEST_RETRIES=0` | `0` | 0 | 1 | Test passes |
| Standalone sets zero before import | `0` | 0 | 1 | Confirmed |

Rerun the distinguishing test cases with:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

The fixture’s environment patch and cleanup provide isolation, but cannot change configuration already captured during import. Startup configuration matches the behavior described in `incident.md`; whether live changes should be supported remains unspecified.

No files were changed, dependencies installed, or external services accessed.
