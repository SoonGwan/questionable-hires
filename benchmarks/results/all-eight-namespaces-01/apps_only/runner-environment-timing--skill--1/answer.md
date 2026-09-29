I’ll use the exorcist skill to compare the actual test and standalone paths, focusing on when the worker reads `REQUEST_RETRIES`. I’ll keep the investigation local and leave existing files unchanged.

The test imports `worker` before `setUp` patches the environment. `worker` reads the retry value during that import. I’ll run the existing test under both startup environments and record the environment, effective retry value, and callback count to confirm that this ordering explains the discrepancy.

The discrepancy is deterministic import timing. [worker.py:3](project/worker.py#L3) reads `REQUEST_RETRIES` once into `RETRIES`. The test imports `worker` before `setUp` changes the environment.

Fresh-process runs using the actual test and worker produced:

| Startup environment | Environment during test | `worker.RETRIES` | Attempts | Result |
|---|---|---|---|---|
| Variable absent | `"0"` | `2` | 3 | FAIL |
| Set to `"0"` before import | `"0"` | `0` | 1 | PASS |

The standalone path also recorded one attempt with the variable set before import. Reproduce the test comparison with:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

`patch.dict` successfully changes and restores the environment, but it cannot recompute the already assigned `worker.RETRIES`. The retry limit therefore allows the initial attempt plus two retries.

No intermittent cache behavior is needed to explain this reproduction. Given the documented startup configuration contract, the test must arrange configuration before import; whether runtime changes should be supported remains unspecified.

No files were changed, dependencies installed, or external services accessed.
