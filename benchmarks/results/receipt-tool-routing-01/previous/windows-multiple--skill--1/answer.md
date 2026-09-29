I’m using the receipt skill to compare the three versions of `windows.py` against the same current tests, retaining native exits and assertion evidence without changing production code.

Verified all six native tests per revision, using identical current `test_windows.py` and:

```text
<TEMP> -B -m unittest -v test_windows
```

HEAD ran once. No tests were skipped.

| Revision | Full commit ID | Native exit | Result |
|---|---|---:|---|
| HEAD~2 | `c4a41f0c97d598fb902f24be2b09ed8ddc602450` | 1 | 4 pass, 2 fail |
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 1 | 5 pass, 1 fail |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 0 | 6 pass |

Actual assertion values establish both changes:

| Test | Expected | HEAD~2 actual | HEAD^ actual | HEAD actual |
|---|---|---|---|---|
| Touching | `[(1, 5)]` | `[(1, 3), (3, 5)]` | `[(1, 5)]` | `[(1, 5)]` |
| Nested | `[(1, 10)]` | `[(1, 3)]` | `[(1, 3)]` | `[(1, 10)]` |

HEAD^ merges touching endpoints; HEAD additionally preserves the containing interval’s endpoint.

Controls passed in every version: chain returned `[(1, 9)]`, disjoint returned `[(1, 3), (5, 7)]`, empty returned `[]`, and input remained `[(5, 7), (1, 3)]`. The returned list was a distinct object in every input-preservation test.

Each native process verified its loaded module beneath:
```text
<WORKSPACE>/.receipt-87l2q41v/
```

| Revision | Copied module | PID |
|---|---|---:|
| HEAD~2 | `before/windows.py` | 69621 |
| HEAD^ | `before_2/windows.py` | 69622 |
| HEAD | `after/windows.py` | 69623 |

Captured output retains all assertion arguments and native exits without truncation. The preservation guard confirmed unchanged project bytes/modes, including Git metadata and skill resources. Scratch copies were removed; no harness or report remains. Final diff checks passed, with only the pre-existing untracked skill files present.
