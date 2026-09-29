I’ll use the exorcist skill to compare the actual test and standalone paths, then run a local probe to identify where their retry settings diverge. I’ll leave existing files unchanged.

The worker reads `REQUEST_RETRIES` when it is imported, and the test imports it before `setUp` runs. I’ll check the effective retry value and record the callback calls during the actual test, then compare fresh processes with the variable absent and set to zero before import.

The discrepancy is deterministic import timing.

[worker.py:3](project/worker.py) reads `REQUEST_RETRIES` once into `RETRIES`. [test_worker.py:4](project/test_worker.py) imports the worker before `setUp` patches the environment.

Fresh-process probes ran the actual unittest setup and worker, recording calls to the test’s callback:

| Environment before import | Environment after `setUp` | Effective `RETRIES` | Attempts |
|---|---|---|---|
| Absent | `0` | `2` | 3 — test fails |
| `0` | `0` | `0` | 1 — test passes |

The standalone reproduction also made one attempt.

`patch.dict` changes the environment and cleanup restores it, but neither updates the already initialized `worker.RETRIES`. No intermittent cache behavior is needed to explain this reproduction.

Rerun the distinction with:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

Startup configuration matches the behavior described in `incident.md`; whether live configuration changes should be supported remains unspecified. No files were modified or external services accessed.
