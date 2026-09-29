I’ll use the exorcist skill to compare the actual test and standalone paths, then probe where their retry settings diverge. I’ll keep all existing files unchanged and use only local Python commands.

The reported results reproduce: the fresh test fails with three calls, and the standalone process makes one. The worker reads the environment at import time, before `setUp` runs. I’ll trace the actual unittest path with the setting absent versus present before import to confirm the effective retry count at delivery.

The discrepancy is deterministic import timing; an intermittent cache problem is unnecessary to explain it.

[worker.py:3](project/worker.py#L3) reads `REQUEST_RETRIES` once into `RETRIES`. [test_worker.py:4](project/test_worker.py#L4) imports the worker before `setUp` patches the environment.

Tracing the actual unittest and its callback in fresh processes showed:

| Setting before import | Environment at delivery | `worker.RETRIES` | Attempts |
|---|---|---|---|
| Absent | `"0"` | `2` | 3 |
| `"0"` | `"0"` | `0` | 1 |

`env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker` reproduced `AssertionError: 3 != 1`. The standalone callback made one attempt with `REQUEST_RETRIES=0` set before import.

The fixture’s environment patch works, and cleanup restores it, but neither updates the already initialized `worker.RETRIES`. Startup configuration explains both outcomes. Whether configuration should change dynamically remains unspecified.

No files were changed, dependencies installed, or external services accessed.
