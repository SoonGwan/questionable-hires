I’ll use the con-artist skill to trace the transaction, test one isolated persistence fault, and verify the stronger assertions against both correct and faulty code.

The existing test checks only the acknowledgment. The native fixtures seed Alice at 100 and Bob at 250 for amounts 7 and 13. `debit` updates SQLite, commits, then returns success based on the update’s row count.

I’ll replace `commit()` with `rollback()` only in the disposable faulty copy. That reaches the real transaction and preserves the success acknowledgment while discarding the balance change.

Both original cases passed despite the faulty transaction leaving Alice at 100. The improved cases pass on correct code and fail on the faulty code at Alice’s balance assertion: actual 100 versus expected 93 and 87. Bob remained at 250 in every run.

I’ll run the prescribed command on the original project, then remove the disposable copies and verify that only the requested test file changed.

Updated [tests/test_debit.py](project/tests/test_debit.py#L1) to verify Alice’s debit and Bob’s unchanged balance through a new connection after return, preserving acknowledgment and both amounts.

The native fixtures and real SQLite transaction executed in disposable copies. In-process checks confirmed the copied module binding. The sole fault replaced `commit()` with `rollback()`, preserving the successful update row count and acknowledgment.

| Tests | Correct code | Faulty code |
|---|---|---|
| Original, amounts 7 and 13 | Both pass | Both pass |
| Improved, amounts 7 and 13 | Both pass | Both fail |

Detecting assertion: `assert balances["alice"] == 100 - amount`.

- Amount 7: actual **100**, expected **93**.
- Amount 13: actual **100**, expected **87**.
- Bob remained **250** throughout.

All runs used the specified Python with `-B -m pytest -q -p no:cacheprovider`; isolated runs added `-p audit_probe -s`. Final native verification: **2 passed**, exit 0.

This establishes detection of the selected rollback fault and visibility from a new connection; it does not establish crash durability or cover README-excluded scenarios.

All scratch copies were removed. Only `tests/test_debit.py` changed; implementation and skill resources were preserved.
