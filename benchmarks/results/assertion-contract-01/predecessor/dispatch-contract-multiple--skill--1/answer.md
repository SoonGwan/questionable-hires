I’m using the con-artist skill to check each fault independently, verify which implementation the native tests load, and test focused regression assertions for any gaps. I’ll remove all audit scratch and preserve the supplied files and Git state.

The two existing tests check ordered return values and payload isolation, including caller state. Neither exercises `ValueError`. I’ll run both against all three faults and verify additional error-propagation and stop-dispatch assertions, alongside a successful-dispatch check.

Existing tests detect **reversed-handlers** and **shared-payload**, but miss **swallowed-error**.

Every check ran in a disposable project-local copy using:

```sh
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v test_dispatch
```

| Implementation | Tests | Assertion failures | Exit |
|---|---:|---:|---:|
| Correct, original tests | 2 | 0 | 0 |
| swallowed-error | 2 | 0 | 0 |
| reversed-handlers | 2 | 2 | 1 |
| shared-payload | 2 | 1 | 1 |
| Correct, augmented tests | 4 | 0 | 0 |
| swallowed-error, augmented tests | 4 | 2 subtest failures | 1 |

**Six native executions, 16 test executions.** The unchanged original correct baseline was reused for all three fault comparisons. Faults were never combined.

- **reversed-handlers:** `test_order` at `test_dispatch.py:7` detects `['second', 'first']` instead of `['first', 'second']`. The result assertion at line 14 also fails.
- **shared-payload:** line 14 detects both results containing the mutated list `[1, 2]`. The caller-state assertion at line 15 is not reached on this variant.
- **swallowed-error:** neither original test raises an error. Additional assertions verified exact `ValueError` type/message, calls equal to `['first', 'fail']`, and unchanged caller state. The faulty implementation fails because no exception reaches the caller and `later` runs. A nearby successful-dispatch regression checks execution order, ordered results, independent nested payloads, and unchanged caller state; it passes on both implementations.

Each native test process verified the copied module path, function code path, and test-global binding to that variant’s actual `dispatch`. All failures above were behavioral assertions; no setup or collection failures occurred.

Whole-project integrity checks confirmed unchanged supplied files and Git metadata, including HEAD/index. All owned scratch was removed; no report, harness, or test changes were retained.
