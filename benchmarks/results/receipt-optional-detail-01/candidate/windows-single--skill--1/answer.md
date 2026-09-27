I’m using the receipt skill to compare isolated copies of `HEAD^` and `HEAD` under the unchanged current tests, retaining each process’s exit status and loaded module path. I’ll remove all comparison scratch before finishing.


The commit changes nested-window handling: merging `(2, 3)` into `(1, 10)` now keeps the end at `10`. I’ll run all six tests once per revision and capture assertion arguments so the passing controls also have concrete values.


Verified: nested windows now retain the enclosing endpoint. All five other controls remain passing.

Each revision ran once with identical current `test_windows.py`, varying only `windows.py`:

```text
<TEMP> -B -m unittest -v test_windows
```

| Revision | Full commit ID | Native result |
|---|---|---|
| HEAD^ | `9910b517fbdf67e0335ae7e92967de94be62d62a` | Exit 1; 6 tests, 1 failure |
| HEAD | `1f8f37f823ac34a0ff36cdd2e6f8a2cc291eeb24` | Exit 0; 6 tests passing |

No tests skipped. Captured assertion values:

| Test | HEAD^ actual | HEAD actual | Expected |
|---|---|---|---|
| nested | `[(1, 3)]` | `[(1, 10)]` | `[(1, 10)]` |
| touching | `[(1, 5)]` | Same | `[(1, 5)]` |
| chain | `[(1, 9)]` | Same | `[(1, 9)]` |
| disjoint | `[(1, 3), (5, 7)]` | Same | `[(1, 3), (5, 7)]` |
| empty | `[]` | Same | `[]` |
| input preserved | `[(5, 7), (1, 3)]` | Same | `[(5, 7), (1, 3)]` |

Both input-preservation tests also observed result `[(1, 3), (5, 7)]` as a distinct object from the source.

Native processes confirmed these loaded modules, relative to the project root:

- HEAD^, PID `14638`: `.receipt-lt65kyyt/before/windows.py`
- HEAD, PID `14639`: `.receipt-lt65kyyt/after/windows.py`

Assertion arguments were observed without changing assertions. Full output and process exits were captured. Scratch was removed; project bytes/modes, Git metadata, and installed skill resources remained unchanged. No harness or report remains.
