I’ll use the con-artist skill to trace the three tests, then run each once against normal code and once against the specified fault in disposable project-local copies. I’ll preserve the originals and remove the scratch files afterward.

The missing-destination tests reach the error handler after debiting account `a`. One checks only the re-raised exception; the other reopens the database and checks balances. The success test never reaches the error handler. I’ll now run the six individual checks, without adding probes or changing test bodies.

Only `test_error_keeps_persisted_balances` detects the specified fault.

| Method | Normal exit | Faulty exit | Detecting assertion or actual observation |
|---|---:|---:|---|
| `test_rejects_missing_destination` | 0 | 0 | Checks `LookupError` matching `'destination missing'`. The retained re-raise satisfies it; persisted balances are unchecked. |
| `test_error_keeps_persisted_balances` | 0 | 1 | `assertEqual(self.balances(), [('a', 100), ('b', 20)])` fails: actual persisted rows are `[('a', 90), ('b', 20)]`. |
| `test_success_moves_balance` | 0 | 0 | Checks persisted rows `[('a', 90), ('b', 30)]` after success. It never exercises the error handler. |

The faulty handler commits the debit before re-raising the missing-destination error. The detecting test reads through a new SQLite connection, confirming that `a` loses 10 with no corresponding credit: the persisted total falls from 120 to 110.

Each method was run separately in both copies using:

```sh
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 \
  -B -E -s -m unittest -v test_ledger.Transfers.<method>
```

Exactly six native test processes ran, each bounded to 20 seconds, using Python 3.9.6 and identical test files and inputs. Each process’s working directory selected its normal or faulty implementation. The only source difference was the handler’s `rollback()` → `commit()`; the re-raise remained.

No grouped suite, stronger probes, or additional faults were run. This establishes sensitivity to this fault for these inputs, not general transaction safety. Originals remained byte-identical, and all owned project-local scratch was removed.
