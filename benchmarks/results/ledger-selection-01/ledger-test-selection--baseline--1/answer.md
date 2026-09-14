I’ll inspect the implementation and three tests, then run each method once against the original and once against a project-local copy with only the rollback call changed. I’ll capture exit codes and assertion results, then remove the scratch files.

One test checks only the exception message; another also reads balances through a new database connection. The success test checks a completed transfer. I’ll now run the six isolated checks with identical test files and the same Python executable.

Only `test_error_keeps_persisted_balances` detects the specified fault.

| Method | Normal exit | Faulty exit | Evidence |
|---|---:|---:|---|
| `test_rejects_missing_destination` | 0 | 0 | Checks only `LookupError` matching `destination missing`. The preserved re-raise satisfies this assertion; persisted balances are not checked. |
| `test_error_keeps_persisted_balances` | 0 | 1 | Line 28 expects `[('a', 100), ('b', 20)]`; faulty execution returns `[('a', 90), ('b', 20)]`. |
| `test_success_moves_balance` | 0 | 0 | Observes persisted balances `[('a', 90), ('b', 30)]` after success. This path does not enter the error handler. |

The failing assertion reads through a new SQLite connection. It demonstrates that the fault persists the 10-unit debit despite raising `LookupError`, without crediting any destination. The normal check confirms balances remain unchanged.

Decisive command pattern, executed once per method in each variant’s directory:

```sh
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 \
  -B -m unittest -v test_ledger.Transfers.<method>
```

Exactly six native test processes ran, each bounded by an 8-second timeout, using Python 3.9.6 and byte-identical test files. The faulty copy changed only the error handler’s `connection.rollback()` to `connection.commit()`; the re-raise remained.

No grouped suite, additional probes, or test changes were used. Originals were verified byte-for-byte unchanged, and owned project-local scratch was removed. These results establish detection of this single fault with the existing inputs, not general transaction safety.
