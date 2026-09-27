I’ll use the receipt skill to compare the three revisions against the unchanged current tests, capture each process’s results and loaded module path, and remove the scratch files afterward.

The changes address two separate behaviors: `HEAD^` merges touching endpoints, and `HEAD` preserves the larger endpoint when one window contains another. I’ll record the assertion arguments during each native run so the evidence includes passing values as well as failures.

My assertion observer used the wrong argument names for `assertIsNot`, causing an instrumentation error in each run. Those runs cannot establish the control result. I’ll correct the temporary observer and rerun all three revisions; production code and tests remain untouched.

Verified all six unchanged current tests against each committed `windows.py`, using:

```text
<TEMP> -B -m unittest -v test_windows
```

| Revision | Full commit ID | Native exit | Result |
|---|---|---:|---|
| HEAD~2 | `c4a41f0c97d598fb902f24be2b09ed8ddc602450` | 1 | 4 pass, 2 fail |
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 1 | 5 pass, 1 fail |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 0 | 6 pass |

Actual assertion values establish the changes:

| Test | HEAD~2 actual | HEAD^ actual | HEAD actual | Expected |
|---|---|---|---|---|
| Touching | `[(1,3),(3,5)]` | `[(1,5)]` | `[(1,5)]` | `[(1,5)]` |
| Nested | `[(1,3)]` | `[(1,3)]` | `[(1,10)]` | `[(1,10)]` |

`HEAD^` fixes touching endpoints; `HEAD` additionally preserves containing endpoints.

All versions pass the controls: chain returns `[(1,9)]`, disjoint returns `[(1,3),(5,7)]`, empty returns `[]`, and input remains `[(5,7),(1,3)]`. The returned list is a different object.

Each native process verified its loaded module beneath project-local `.receipt-native-vfvf5w2t/`:

- HEAD~2: `before/windows.py`, PID 15559
- HEAD^: `middle/windows.py`, PID 15562
- HEAD: `after/windows.py`, PID 15565

Captured output retains full absolute paths, source hashes, identical test hashes, assertion arguments and exits. Initial observer attempts each exited 1 due to an instrumentation error; the corrected runs above provide the valid comparison.

All scratch was removed. Original bytes, modes and entries—including Git metadata and skill resources—were unchanged. Diff checks passed; no harness or report remains.
