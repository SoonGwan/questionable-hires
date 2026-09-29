I’ll use the exorcist skill to compare the actual unittest setup with the standalone command and capture deterministic local evidence without changing files.

The worker reads `REQUEST_RETRIES` during import, which happens before `setUp` changes the environment. I’ll run the existing test, then record the environment, effective retry count, and callback calls with the setting applied before versus after import.

The discrepancy is deterministic **configuration timing**.

[worker.py](project/worker.py#L3) reads `REQUEST_RETRIES` once at import. [test_worker.py](project/test_worker.py#L4) imports it before `setUp` patches the environment. Thus `setUp` sets the environment to `'0'`, but `worker.RETRIES` remains `2`, producing three attempts.

Fresh-process evidence using the actual test and a recording wrapper around its callback:

| Environment before import | Environment after actual `setUp` | `worker.RETRIES` | Attempts | Result |
|---|---|---|---|---|
| Absent | `'0'` | `2` | 3 | FAIL |
| `'0'` | `'0'` | `0` | 1 | PASS |

The incident’s standalone scenario also recorded one attempt and propagated `RuntimeError`.

Rerun the distinguishing test cases:

```sh
env -u REQUEST_RETRIES python3 -B -m unittest -v test_worker
REQUEST_RETRIES=0 python3 -B -m unittest -v test_worker
```

The fixture’s environment patch and cleanup work, but neither recomputes the imported constant. No intermittent cache problem is needed to explain this reproduction.

For the documented startup configuration behavior, set the environment before import. Whether runtime configuration changes should be supported remains unspecified.

No files were changed, dependencies installed, or external services accessed.
