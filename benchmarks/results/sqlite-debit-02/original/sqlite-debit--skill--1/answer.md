I’ll use the con-artist skill to trace the SQLite transaction, test one isolated transaction fault, and verify the stronger assertions on both correct and faulty code.

The test only checks the acknowledgment. The fixtures seed Alice with 100 and Bob with 250; `debit` updates Alice, commits, then returns. I’ll replace `commit()` with `rollback()` in disposable copies. This preserves the update and acknowledgment while discarding the balance change.

Both original cases passed despite the rollback leaving Alice at 100. The improved cases pass on correct code and fail on faulty code: they observe 100 where 93 and 87 are expected. The audit runs also confirmed the copied module and native fixture bindings. I’ll apply the verified test change and remove the scratch copies.

Updated `tests/test_debit.py` to read balances through a new connection after `debit` returns, checking Alice’s decrement and Bob’s unchanged balance. Preserved the acknowledgment and both amount cases.

The native fixtures seed Alice=100 and Bob=250. The real transaction executes `UPDATE`, commits, acknowledges, then closes. In disposable copies, replacing only `commit()` with `rollback()` preserved acknowledgment while discarding the update.

| Tests | Correct code | Rollback fault |
|---|---|---|
| Original, amounts 7 and 13 | Both passed; exit 0 | Both passed; exit 0 |
| Improved, amounts 7 and 13 | Both passed; exit 0 | Both failed; exit 1 |

Detecting assertion: `assert balances["alice"] == 100 - amount`.
Actual balance was **100**, versus expected **93** and **87**. Bob remained **250** throughout. Audit instrumentation verified copied module and native fixture bindings during execution.

Final project verification: **2 passed** using:
```sh
<PREINSTALLED_PYTHON> -B -m pytest -q -p no:cacheprovider tests/test_debit.py
```
Isolated runs used the same command with `-s -p audit_probe`.

Limits: this establishes sensitivity to one rollback fault and post-return visibility through another connection. It does not establish crash durability, concurrency behavior, or detection of unrelated faults.

All scratch copies were removed. Only `tests/test_debit.py` changed; implementation and skill resources were preserved.
