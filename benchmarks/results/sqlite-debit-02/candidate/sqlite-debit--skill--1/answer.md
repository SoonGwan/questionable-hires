I’m using the con-artist skill to trace the persisted-debit check, run one isolated transaction fault, and verify the stronger test against both versions.

The current test checks only the acknowledgment. The fixtures seed Alice with 100 and Bob with 250, with debit amounts 7 and 13. The implementation updates Alice, commits, then returns.

I’ll replace `commit()` with `rollback()` only in a disposable copy. SQLite will still report one updated row, so the acknowledgment can remain successful even though the balance change is discarded. The stronger test will read both balances through a new connection after the call.

**The original tests missed an acknowledged but unpersisted debit.** Updated `tests/test_debit.py` to read Alice and Bob through a new SQLite connection after `debit` returns, preserving the acknowledgment assertion and both amounts.

Native fixtures seed Alice=100 and Bob=250. The real transaction updates Alice, commits, and acknowledges using `rowcount`. In disposable copies, replacing only `commit()` with `rollback()` preserved the acknowledgment while discarding the update. In-process checks verified the copied module bindings; native fixtures ran unchanged.

| Tests | Correct code | Rollback fault |
|---|---|---|
| Original, amounts 7 and 13 | 2 passed; exit 0 | 2 passed; exit 0 |
| Improved, amounts 7 and 13 | 2 passed; exit 0 | 2 failed; exit 1 |

Detecting assertion: `assert balances["alice"] == 100 - amount`.

- Amount 7: actual **100**, expected **93**.
- Amount 13: actual **100**, expected **87**.

Bob’s expected balance remains **250**; both correct-code cases passed that assertion.

Final verification: **2 passed**, using:
```sh
<PREINSTALLED_PYTHON> -B -m pytest -q -p no:cacheprovider tests/test_debit.py
```

Only the requested test file changed; all scratch copies were removed. This audit establishes sensitivity to this rollback fault and fresh-connection visibility, not crash durability, concurrency, or the README’s excluded cases.
