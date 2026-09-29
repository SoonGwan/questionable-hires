I’ll read the exorcist skill and trace the worker’s actual test setup, then run local experiments to distinguish cache effects from environment timing without changing files.

The discrepancy is deterministic **configuration timing**, with no intermittent cache needed to explain it.

[test_worker.py](project/test_worker.py#L4) imports `worker` before `setUp` runs. At import, [worker.py](project/worker.py#L3) reads the absent environment variable and assigns `RETRIES = 2`. `setUp` later changes the environment to `"0"`, but `deliver` still uses that previously assigned integer.

Local evidence using the actual worker and fixture:

| Experiment | Result |
|---|---|
| Fresh unittest process, variable absent | Fails: `3 != 1` |
| Same unittest, variable set to `0` before startup | Passes |
| Actual `setUp`, following import with variable absent | Environment is `"0"`; `worker.RETRIES` remains `2`; callback runs three times |
| Standalone, variable `0` before import | `worker.RETRIES` is `0`; callback runs once |

Rerun the decisive comparison:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
env REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

The fixture’s cleanup correctly restores the environment; it cannot change an already assigned module constant. Under the documented startup configuration behavior, configure the environment before import when testing that behavior. Whether live configuration changes should be supported remains unspecified.

No files changed, dependencies installed, or external services accessed.
