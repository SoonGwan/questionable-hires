I’ll read the exorcist skill and trace the worker’s configuration through the test setup, then run local experiments without changing existing files.

The worker reads `REQUEST_RETRIES` at import, while the test sets it later in `setUp`. I’ll reproduce both attempt counts and inspect the environment alongside `worker.RETRIES` during the actual test setup to check that timing boundary.

The discrepancy is deterministic import timing.

[worker.py](project/worker.py#L3) reads the environment once into `RETRIES`. [test_worker.py](project/test_worker.py#L4) imports it before `setUp`, so the default `2` is already stored when the environment patch runs.

Observed using the actual setup and inherited test:

| Boundary | Environment | `worker.RETRIES` |
|---|---|---|
| Before `setUp` | absent | 2 |
| After `setUp` | `'0'` | 2 |
| After cleanup | absent | 2 |

Rerunnable controls:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
# FAIL: 3 != 1

env REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
# PASS
```

The standalone callback also recorded **one attempt** when the variable was set before import.

`patch.dict` correctly changes and restores the environment; it cannot update the integer already stored in `worker.RETRIES`. No intermittent cache problem is needed to explain this reproduction.

Given the documented startup configuration behavior, configure the environment before import when testing startup behavior, or patch `worker.RETRIES` when testing the retry loop. Whether live environment changes should be supported remains unspecified.

No files changed, dependencies installed, or external services accessed.
