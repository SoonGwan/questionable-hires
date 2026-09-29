I’m using the receipt skill to compare both committed versions of `windows.py` against the unchanged current tests, retaining native exit codes and assertion results.


Verified: HEAD fixes nested windows being shortened. All five other controls pass in both revisions.

Both native processes ran all six unchanged current tests once using:
```sh
<TEMP> -B -m unittest -v test_windows
```

| Revision | Full commit ID | Native exit | Results |
|---|---|---:|---|
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 1 | 5 passed, nested failed |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 0 | 6 passed |

Actual assertion values:

| Test | HEAD^ actual | HEAD actual | Expected |
|---|---|---|---|
| Nested | `[(1, 3)]` | `[(1, 10)]` | `[(1, 10)]` |
| Chain | `[(1, 9)]` | Same | `[(1, 9)]` |
| Disjoint | `[(1, 3), (5, 7)]` | Same | `[(1, 3), (5, 7)]` |
| Empty | `[]` | Same | `[]` |
| Input preserved | `[(5, 7), (1, 3)]` | Same | `[(5, 7), (1, 3)]` |
| Touching | `[(1, 5)]` | Same | `[(1, 5)]` |

The input-preservation test also confirmed in both processes that result `[(1, 3), (5, 7)]` and source `[(5, 7), (1, 3)]` were distinct objects.

Each process verified its loaded module under the project root:

- HEAD^, PID `67084`: `.receipt-9fvhkcct/before/windows.py`
- HEAD, PID `67085`: `.receipt-9fvhkcct/after/windows.py`

Only `windows.py` varied; current `test_windows.py` was identical in both copies. The change uses `max(previous_end, end)` to retain the enclosing window’s endpoint.

No tests were skipped; captured output was complete. Preservation checks confirmed original bytes/modes, Git metadata and skill resources unchanged. Scratch was removed, no harness or report remains, and `git diff --check` passed.
