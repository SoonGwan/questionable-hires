I’ll read the receipt skill, then test both revisions’ `windows.py` against the same current test file, capturing exits, assertion values, and loaded module paths.

Both revisions ran all six tests. Only nested windows changed: `HEAD^` returned `[(1, 3)]` where `[(1, 10)]` was expected; `HEAD` passed. The five controls passed in both runs. The helper captured assertion values and loaded module paths, confirmed preservation, and removed its scratch copies.

Verified using the receipt skill. Only committed `windows.py` varied; both runs used identical current `test_windows.py` and:

```text
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v test_windows
```

| Revision | Full commit ID | Native exit | Results |
|---|---|---:|---|
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 1 | 5 passed, nested failed |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 0 | All 6 passed |

Actual assertion values:

| Behavior | HEAD^ | HEAD | Expected |
|---|---|---|---|
| Nested | `[(1, 3)]` | `[(1, 10)]` | `[(1, 10)]` |
| Chain | `[(1, 9)]` | Same | `[(1, 9)]` |
| Disjoint | `[(1, 3), (5, 7)]` | Same | `[(1, 3), (5, 7)]` |
| Empty | `[]` | Same | `[]` |
| Input preserved | `[(5, 7), (1, 3)]` | Same | `[(5, 7), (1, 3)]` |
| Touching | `[(1, 5)]` | Same | `[(1, 5)]` |

Both identity assertions also passed: result `[(1, 3), (5, 7)]` and source `[(5, 7), (1, 3)]` were different objects.

Each native process confirmed its loaded module, relative to the project root:

- HEAD^, PID 1666: `.receipt-9pscxk63/before/windows.py`
- HEAD, PID 1667: `.receipt-9pscxk63/after/windows.py`

The change preserves the larger endpoint when merging nested windows. All five controls remained passing; neither run skipped tests.

Preservation checks confirmed original bytes/modes unchanged, including Git metadata and skill resources. Scratch was removed; no code edits, harness, or report remain.
