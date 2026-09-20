I’ll use the exorcist skill to compare the existing test with the standalone reproduction and trace when the worker reads its retry setting. I’ll keep all existing files unchanged and run only local Python checks.

The discrepancy is deterministic import order, not evidence of an intermittent cache problem.

[worker.py](project/worker.py#L3) reads `REQUEST_RETRIES` once at import. [test_worker.py](project/test_worker.py#L4) imports it before `setUp` patches the environment.

Fresh-process checks using the actual test and its actual `setUp` showed:

| Environment before import | After `setUp` | Effective `worker.RETRIES` | Result |
|---|---|---:|---|
| Absent | `REQUEST_RETRIES=0` | 2 | 3 attempts; test fails |
| `REQUEST_RETRIES=0` | `REQUEST_RETRIES=0` | 0 | 1 attempt; test passes |

The standalone reproduction also recorded exactly one attempt.

The environment patch works, and cleanup restores it, but neither updates the already initialized `worker.RETRIES`. `deliver` executes `RETRIES + 1` attempts.

Rerun the distinguishing controls:
```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

Given the documented startup configuration contract, the test must configure the environment before import or patch `worker.RETRIES` to test delivery behavior. Whether runtime configuration changes should work remains unspecified.

No existing files changed, dependencies installed, or external services accessed.
