I’ll use the con-artist skill to trace the transaction and fixtures, test one isolated persistence fault, and strengthen the assertions. I’ll remove the scratch copies afterward.



The existing test checks only the acknowledgment. The fixture seeds Alice with 100 and Bob with 250; `debit` updates Alice, commits, then returns success based on the update’s row count.

I’ll replace `commit()` with `rollback()` only in a disposable copy. This should preserve the successful acknowledgment while leaving Alice’s stored balance unchanged. I’ll verify the module loaded by pytest and inspect the database after each test call.



Both original cases passed despite the rollback leaving Alice at 100. The improved cases pass on correct code and fail on the fault: Alice is 100 instead of 93 or 87. Bob remains 250.

I’ll now run the improved test in the original project, remove the copies, and verify that only `tests/test_debit.py` changed.



Updated [tests/test_debit.py](project/tests/test_debit.py#L1) to check Alice’s persisted balance and Bob’s unchanged balance through a new connection after `debit` returns. Preserved the acknowledgment assertion and both amounts.

**The original tests missed the persistence fault.** Native fixtures seed Alice=100 and Bob=250. The real function executes SQLite `UPDATE`, commits, and acknowledges using `rowcount`. Replacing only `commit()` with `rollback()` in a disposable copy preserves that acknowledgment without persisting the debit. In-process probes verified copied-module provenance and database balances.

| Tests / implementation | Amount 7 | Amount 13 | Exit |
|---|---|---|---|
| Original / correct | Pass | Pass | 0 |
| Original / faulty | Pass | Pass | 0 |
| Improved / correct | Pass | Pass | 0 |
| Improved / faulty | Fail | Fail | 1 |

Detecting assertion: `assert balances["alice"] == 100 - amount`.

- Amount 7: actual **100**, expected **93**.
- Amount 13: actual **100**, expected **87**.
- Bob remained **250** throughout.

All runs used:
```sh
<PREINSTALLED_PYTHON> -B -m pytest -q -p no:cacheprovider tests/test_debit.py
```

Final original-project run: **2 passed**. Scratch copies were removed; file hashes confirmed only `tests/test_debit.py` changed.

Scope: one reachable rollback fault and post-return visibility from another connection. This does not establish crash durability or cover concurrency, overdrafts, missing accounts, migrations, monetary representation, or sensitivity to a separate wrong-account fault.
