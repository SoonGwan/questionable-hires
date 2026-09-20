I’ll use the exorcist skill to compare the actual test and worker behavior with the standalone command, using local evidence and leaving existing files unchanged.

The discrepancy is deterministic: **configuration is read at import time, before `setUp` runs.**

[worker.py](project/worker.py#L3) sets `RETRIES` once. [test_worker.py](project/test_worker.py#L4) imports it while `REQUEST_RETRIES` is absent, so `RETRIES=2`. The fixture later changes the environment to `"0"`, but `deliver` still uses `range(2 + 1)`.

Local evidence using the actual worker and test setup:

| Observation | Environment | `worker.RETRIES` | Result |
|---|---|---|---|
| After test module import | absent | 2 | |
| After actual `setUp` | `"0"` | 2 | Actual test fails: `3 != 1` |
| Temporarily patch effective `worker.RETRIES` | `"0"` | 0 | Same test passes: one attempt |
| Standalone, environment set before import | `"0"` | 0 | One attempt |

The baseline command was `env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker`.

The fixture’s environment patch and cleanup isolate environment changes; they do not recompute an already assigned module variable. No intermittent cache behavior is needed to explain this reproduction.

Given the startup configuration contract in [incident.md](project/incident.md), tests should set the environment before importing the worker or patch `worker.RETRIES` when testing delivery behavior. Whether configuration should update live remains unspecified.

No files were changed, dependencies installed, or external services accessed.
