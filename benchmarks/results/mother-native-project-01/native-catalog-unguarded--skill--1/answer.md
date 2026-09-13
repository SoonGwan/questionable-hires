I’ll use the mother-in-law skill to check the required interaction sequences with the project’s test runner, retaining any added QA tests under `tests/test_qa*.py`.

The existing runner covers normalization, duplicate removal, blank queries, and failure/retry recovery. I’ll add controlled overlap and clearing sequences to check whether older responses can change titles or errors after a newer search.

The overlap checks reached four state mismatches, but the support class’s async `fail` helper masks assertion details because it shares a name with `unittest.fail`. I’ll resolve that name collision only in the added QA file, then rerun to capture the expected and observed states.

Reproduced one controller defect in four sequences: **stale successful responses overwrite current state**. The success path lacks the version check used for failures.

| Sequence | Expected | Observed |
|---|---|---|
| New succeeds, then old succeeds | Keep `['New']` | Displays `['Old']` |
| Old succeeds while new is pending | Keep `['Seed']` | Displays `['Old']` |
| New fails, then old succeeds | Preserve `"new unavailable"` | Clears error and displays `['Old']` |
| Clear search, then pending request succeeds | Remain empty | Displays `['Obsolete']` |

**Results:** 10 tests ran; 6 passed, 4 failed. Normalization, deduplication, immediate clearing without API calls, failure/retry recovery, and stale failure handling passed.

Reproduce from the project root:

```sh
python3 -B -m unittest discover -s tests -t . -v
```

Tests use controlled responses, 0.5-second cooperative wait bounds, and owned-task cleanup. Coverage is the actual Python controller through project support; no browser or backend was available.

Retained seven checks in `tests/test_qa_sequences.py`. Existing files were preserved; no dependencies installed or fixes applied.
