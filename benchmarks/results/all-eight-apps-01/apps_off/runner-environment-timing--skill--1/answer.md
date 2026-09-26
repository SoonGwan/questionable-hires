I’m using the exorcist skill to compare the actual test setup with the standalone command and identify where their retry settings diverge. I’ll keep existing files unchanged and run only local Python checks.

I’ll use the existing unittest as the primary reproduction, then compare it with the command in `incident.md`. That preserves the import order and `setUp` behavior that may explain the difference.

The discrepancy is deterministic **import-time configuration**, not evidence of an intermittent cache problem.

[test_worker.py:4](project/test_worker.py) imports `worker` before `setUp`. At import, [worker.py:3](project/worker.py) reads `REQUEST_RETRIES` into `RETRIES` once. Setting the environment later does not update that integer.

Using fresh Python processes and the actual test, with a recording callback forwarding to its original callback:

| Startup environment | Environment during delivery | Effective `worker.RETRIES` | Attempts |
|---|---|---:|---:|
| Absent | `0` from `setUp` | 2 | 3 |
| `0` | `0` from `setUp` | 0 | 1 |

The standalone reproduction also produced one attempt because it set `0` **before importing worker**.

Rerunnable comparison:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

The first fails with `3 != 1`; the second passes. `-B` prevents bytecode writes.

The test’s environment patch works, and its cleanup restores the environment, but neither changes the already initialized `worker.RETRIES`. Startup configuration matches the behavior described in `incident.md`; whether live updates should work remains unspecified.

No files were changed, dependencies installed, or external services accessed.
