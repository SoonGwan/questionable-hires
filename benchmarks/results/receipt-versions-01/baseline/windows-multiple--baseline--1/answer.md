I’ll run each committed `windows.py` against the same current test file, capture the module path, exit status, and assertion results, then remove the scratch files.

Verified all six native unittest tests once per revision using the specified interpreter and byte-identical current `test_windows.py`. Assertion arguments were captured by tracing; assertions were unchanged.

| Revision | Full commit ID | Passed | Native exit |
|---|---|---:|---:|
| HEAD~2 | `c4a41f0c97d598fb902f24be2b09ed8ddc602450` | 4/6 | 1 |
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 5/6 | 1 |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 6/6 | 0 |

Actual assertion values:

| Test | Expected | HEAD~2 | HEAD^ | HEAD |
|---|---|---|---|---|
| touching | `[(1, 5)]` | `[(1, 3), (3, 5)]` | `[(1, 5)]` | `[(1, 5)]` |
| nested | `[(1, 10)]` | `[(1, 3)]` | `[(1, 3)]` | `[(1, 10)]` |
| chain | `[(1, 9)]` | Same | Same | Same |
| disjoint | `[(1, 3), (5, 7)]` | Same | Same | Same |
| empty | `[]` | Same | Same | Same |
| input preserved | `[(5, 7), (1, 3)]` | Same | Same | Same |

The input-preservation identity assertion also passed throughout: result `[(1, 3), (5, 7)]` was a distinct object from source.

HEAD^ changes `<` to `<=`, fixing touching-window merging. HEAD uses `max(previous_end, end)`, fixing nested windows that previously shortened the containing window. All four control tests remain passing.

Each process reported its loaded module beneath the project’s `.window-verification-m8ua7_3j/` directory:

- HEAD~2: `head_minus_2/windows.py`
- HEAD^: `head_parent/windows.py`
- HEAD: `head/windows.py`

Loaded module hashes matched the corresponding Git contents. Full paths, hashes, assertion values, and native exits are retained in captured output.

Scratch was removed. Original file bytes, modes, and file set were verified unchanged; no harness or report remains.
