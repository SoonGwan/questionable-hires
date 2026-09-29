I’m using the receipt skill to compare all three revisions under the unchanged current tests, retaining each native exit status and assertion result. I’ll remove the comparison scratch files before finishing.


Verified using the receipt comparison helper. Only `windows.py` varied; every process used identical current `test_windows.py` and ran:

```sh
<TEMP> -B -m unittest -v test_windows
```

| Revision | Full commit ID | Native exit | Results |
|---|---|---:|---|
| HEAD~2 | `c4a41f0c97d598fb902f24be2b09ed8ddc602450` | 1 | 4 pass, 2 fail |
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 1 | 5 pass, 1 fail |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 0 | 6 pass |

All six tests ran per revision, without skips. HEAD ran once.

Actual assertion values:

| Test | HEAD~2 actual | HEAD^ actual | HEAD actual | Expected |
|---|---|---|---|---|
| Touching | `[(1,3),(3,5)]` | `[(1,5)]` | `[(1,5)]` | `[(1,5)]` |
| Nested | `[(1,3)]` | `[(1,3)]` | `[(1,10)]` | `[(1,10)]` |
| Chain | `[(1,9)]` | Same | Same | `[(1,9)]` |
| Disjoint | `[(1,3),(5,7)]` | Same | Same | `[(1,3),(5,7)]` |
| Empty | `[]` | Same | Same | `[]` |
| Input preserved | `[(5,7),(1,3)]` | Same | Same | `[(5,7),(1,3)]` |

The input-preservation identity assertion also passed everywhere: result `[(1,3),(5,7)]` and source `[(5,7),(1,3)]` were different objects.

HEAD^ fixes touching endpoints through `<=`. HEAD additionally preserves containing endpoints through `max(previous_end, end)`. The four control tests remain passing throughout.

Each native process confirmed its loaded module beneath `<WORKSPACE>/`:

| Revision | PID | Copied module |
|---|---:|---|
| HEAD~2 | 63904 | `.receipt-x1nnu8gg/before/windows.py` |
| HEAD^ | 63905 | `.receipt-x1nnu8gg/before_2/windows.py` |
| HEAD | 63906 | `.receipt-x1nnu8gg/after/windows.py` |

Captured output includes complete assertion observations and native exits, with no truncation or timeouts. Preservation checks reported unchanged original bytes/modes and project tree, including Git metadata and installed skill resources. Scratch was removed; no harness or report remains. Final diff checks passed.
