I’ll use the receipt skill to compare HEAD^ and HEAD under the same current tests, capture both native runs, and remove the scratch files afterward.

Verified: HEAD fixes nested windows shrinking the enclosing interval. All five control tests remain passing.

Both revisions ran all six unchanged current tests once, with no skips, using:
```sh
<TEMP> -B -m unittest -v test_windows
```

| Revision | Full commit ID | Native exit | Result |
|---|---|---:|---|
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 1 | 5 passed, nested failed |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 0 | 6 passed |

Actual assertion values were captured:

| Test | HEAD^ actual | HEAD actual | Expected |
|---|---|---|---|
| Nested | `[(1, 3)]` | `[(1, 10)]` | `[(1, 10)]` |
| Chain | `[(1, 9)]` | Same | `[(1, 9)]` |
| Disjoint | `[(1, 3), (5, 7)]` | Same | `[(1, 3), (5, 7)]` |
| Empty | `[]` | Same | `[]` |
| Touching | `[(1, 5)]` | Same | `[(1, 5)]` |
| Input preserved | `[(5, 7), (1, 3)]` | Same | `[(5, 7), (1, 3)]` |

In both versions, the identity assertion also passed: result `[(1, 3), (5, 7)]` and source `[(5, 7), (1, 3)]` were distinct objects.

Each native process confirmed its loaded module, relative to the project root:

- HEAD^, PID `62238`: `.receipt-gdoahj1p/before/windows.py`
- HEAD, PID `62239`: `.receipt-gdoahj1p/after/windows.py`

Only revision-specific `windows.py` varied. The change uses `max(previous_end, end)` to retain the enclosing endpoint.

The preservation guard confirmed original bytes/modes unchanged, including skill resources and Git metadata. Scratch was removed; no harness or report remains. Final diff checks passed.
