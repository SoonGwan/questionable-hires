I’m using the receipt skill to compare `HEAD^` and `HEAD` under the same current tests, capture native exits and assertion values, and remove the comparison scratch afterward.

Verified: `HEAD` fixes nested windows shrinking the merged endpoint.

| Revision | Full commit ID | Native result |
|---|---|---|
| `HEAD^` | `9910b517fbdf67e0335ae7e92967de94be62d62a` | Exit **1**; 5 passed, nested failed |
| `HEAD` | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | Exit **0**; all 6 passed |

Each revision ran once with identical current `test_windows.py`, varying only `windows.py`, using:

```sh
<TEMP> -B -m unittest -v test_windows
```

Captured assertion values:

| Behavior | `HEAD^` actual | `HEAD` actual | Expected |
|---|---|---|---|
| Nested | `[(1, 3)]` | `[(1, 10)]` | `[(1, 10)]` |
| Touching | `[(1, 5)]` | Same | `[(1, 5)]` |
| Chain | `[(1, 9)]` | Same | `[(1, 9)]` |
| Disjoint | `[(1, 3), (5, 7)]` | Same | `[(1, 3), (5, 7)]` |
| Empty | `[]` | Same | `[]` |
| Input preserved | `[(5, 7), (1, 3)]` | Same | `[(5, 7), (1, 3)]` |

Both identity assertions passed: result `[(1, 3), (5, 7)]` and source `[(5, 7), (1, 3)]` were distinct objects.

Native processes confirmed loaded modules under project root `<WORKSPACE>`:

- PID **61363**, `HEAD^`: `.receipt-m3q6ajxy/before/windows.py`
- PID **61364**, `HEAD`: `.receipt-m3q6ajxy/after/windows.py`

No skips, timeouts, or truncated output. The change uses `max(previous_end, end)`, preserving the outer endpoint. All five controls remain passing.

Preservation checks confirmed unchanged original bytes/modes, including Git metadata and skill resources. Scratch was removed; no harness or report remains. Final diff and whitespace checks passed.
