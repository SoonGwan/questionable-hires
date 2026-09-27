I’m using the receipt skill to compare both committed versions of `windows.py` under the same current tests, capture native results and module identities, and remove the comparison scratch files afterward.

Verified: HEAD fixes nested windows shrinking an existing interval by using `max(previous_end, end)`.

Both revisions ran all six unchanged current tests once, with no skips:
```text
<TEMP> -B -m unittest -v test_windows
```

| Revision | Full commit ID | Native exit | Result |
|---|---|---:|---|
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | 1 | 5 pass, nested fails |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | 0 | All 6 pass |

Assertion values below follow from unchanged passing assertions; the before failure explicitly printed `[(1, 3)] != [(1, 10)]`.

| Behavior | HEAD^ actual | HEAD actual / expected |
|---|---|---|
| Nested | `[(1, 3)]` | `[(1, 10)]` |
| Touching | `[(1, 5)]` | Same |
| Overlap chain | `[(1, 9)]` | Same |
| Disjoint, sorted | `[(1, 3), (5, 7)]` | Same |
| Empty | `[]` | Same |
| Input preserved | Source `[(5, 7), (1, 3)]`; result is a distinct object | Same |

Each native process confirmed its loaded module under project root `<WORKSPACE>`:

- PID `13653`: `.receipt-jcrz5m8e/before/windows.py`
- PID `13654`: `.receipt-jcrz5m8e/after/windows.py`

Only committed `windows.py` varied. Both copies used identical current `test_windows.py` bytes.

The project preservation check passed, including original bytes/modes and skill resources. Scratch was removed; no harness or report remains. Working-tree diff was empty and `git diff --check` exited 0.
