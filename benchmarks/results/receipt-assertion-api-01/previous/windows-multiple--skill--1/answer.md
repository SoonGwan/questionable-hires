I’ll use the receipt skill to compare all three revisions against the unchanged current tests, capturing each process’s exit status, assertion values, and loaded module path.


Verified all three revisions using identical current `test_windows.py`, varying only `windows.py`. Each native process ran all six tests, with no skips, using:

```sh
/opt/homebrew/opt/python@3.11/bin/python3.11 -B -m unittest -v test_windows
```

| Revision | Full commit ID | Native exit | Result |
|---|---|---:|---|
| HEAD~2 | `c4a41f0c97d598fb902f24be2b09ed8ddc602450` | 1 | 4 pass, 2 fail |
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 1 | 5 pass, 1 fail |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 0 | 6 pass |

Actual assertion results:

| Test | Expected | HEAD~2 | HEAD^ | HEAD |
|---|---|---|---|---|
| Touching | `[(1, 5)]` | `[(1, 3), (3, 5)]` | `[(1, 5)]` | `[(1, 5)]` |
| Nested | `[(1, 10)]` | `[(1, 3)]` | `[(1, 3)]` | `[(1, 10)]` |

HEAD^ changes `<` to `<=`, fixing touching endpoints. HEAD adds `max(previous_end, end)`, fixing nested intervals.

Controls passed throughout: chain → `[(1, 9)]`; disjoint → `[(1, 3), (5, 7)]`; empty → `[]`; input remains `[(5, 7), (1, 3)]`, with a distinct result object.

Each native process verified its loaded module beneath the project directory:

| Revision | PID | Copied module |
|---|---:|---|
| HEAD~2 | 27614 | `.receipt-gfy0t00b/before/windows.py` |
| HEAD^ | 27615 | `.receipt-gfy0t00b/before_2/windows.py` |
| HEAD | 27616 | `.receipt-gfy0t00b/after/windows.py` |

HEAD ran once. Captured output retains native exits and assertion failures without truncation. The preservation guard confirmed unchanged original bytes/modes, including skill resources and Git metadata. All comparison scratch was removed; no harness or report remains.
