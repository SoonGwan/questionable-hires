I’ll use the exorcist skill to compare the actual test setup with the standalone command and check where their retry settings diverge. I’ll keep all probes local and leave existing files unchanged.

**The discrepancy is deterministic import timing, with no evidence of an intermittent cache problem.**

[worker.py](project/worker.py#L3) reads `REQUEST_RETRIES` once into `RETRIES`. [test_worker.py](project/test_worker.py#L4) imports it before `setUp` patches the environment. Consequently, `deliver` still uses `RETRIES=2`: one initial attempt plus two retries.

Local evidence using the actual test and worker:

| Probe | Result |
|---|---|
| Fresh unittest process, variable absent | Fails: `3 != 1` |
| Observe actual test at `deliver` entry | Environment is `'0'`; `worker.RETRIES` is `2` |
| Same test, temporarily patch only `worker.RETRIES=0` | Passes |
| Restore constant and repeat in same process | Fails again: `3 != 1` |
| Set environment to `0` before starting unittest | Passes |
| Standalone callback, environment set before import | Exactly one call |

`patch.dict` correctly changes and restores the environment; it cannot recompute an already assigned module constant.

Given the documented startup configuration behavior, configure the environment before importing the worker, or patch `worker.RETRIES` in this unit test. Reading configuration on every delivery would be a separate behavior change; live updates are unspecified.

No existing files were modified, dependencies installed, or external services accessed. Python bytecode writes were disabled.
