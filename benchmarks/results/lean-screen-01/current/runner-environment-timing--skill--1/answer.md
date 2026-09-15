I’ll use the exorcist skill to compare the actual test setup with the standalone command and capture deterministic local evidence without changing existing files.

The test imports `worker` before `setUp` changes the environment. `worker` reads `REQUEST_RETRIES` once at import. I’ll run the original test, then record the effective retry value and callback count through that same test setup and the standalone path.

**The discrepancy is deterministic import ordering.**

[worker.py](project/worker.py#L3) reads `REQUEST_RETRIES` once into `RETRIES`. [test_worker.py](project/test_worker.py#L4) imports it before `setUp` patches the environment.

Local evidence using the actual test and worker:

| Process configuration | Environment at delivery | `worker.RETRIES` | Attempts |
|---|---|---|---|
| Variable absent before import; actual test setup | `0` | `2` | 3 |
| Variable `0` before import | `0` | `0` | 1 |

The original test failed with `AssertionError: 3 != 1`. Recording its real callback confirmed three attempts. The standalone callback ran once, and the original test also passed in that process.

Reproduce the test contrast:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
env REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

The fixture’s environment patch works, and cleanup restores it; neither updates the already initialized `worker.RETRIES`. No intermittent cache mechanism is needed to explain this reproduction.

[incident.md](project/incident.md#L1) specifies startup configuration. Whether runtime changes should be supported remains unspecified.

No files changed, dependencies installed, or external services accessed.
