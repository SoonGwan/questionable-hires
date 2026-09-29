I’ll use the con-artist skill to trace the upload binding, run the existing tests against correct and isolated faulty code, and check whether a fresh-connection assertion detects the lost commit. I’ll preserve the originals and remove the disposable copies.


The receipt tests check only the acknowledgment. The endpoint directly binds `ledger.write_event`, which commits the insert before closing the connection. The project contract requires the exact rows to be visible through a new connection after upload returns.

I’ll omit only the commit in a disposable copy and verify the bindings inside each native test run. If the tests still pass, I’ll add the same complete-row assertion to both copies.


The existing receipt tests **do not detect a lost commit**: both pass with `connection.commit()` omitted, while acknowledgment and connection closing remain unchanged.

Four native runs used `python3 -B -m unittest -v test_receipts audit_binding`:

| Tests | Correct code | Commit omitted |
|---|---|---|
| Existing | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger | 2 passed, exit 0 | 1 assertion failure, exit 1 |

Each process verified `test_receipts.accept → endpoint.handle_upload → ledger.write_event` and the copied module paths. Runtime tracing confirmed the writer was reached and the connection closed.

The stronger binary-upload test reads through a new SQLite connection after the actual upload, using `ORDER BY id`, then asserts:
```python
self.assertEqual(rows, [(10, b'previous'), (20, b'\x00\xffnew')])
```

Correct code passed. Faulty code returned only `[(10, b'previous')]`, failing specifically for missing committed data—not setup or import errors.

Original bytes and modes were preserved; all owned disposable copies were removed.
