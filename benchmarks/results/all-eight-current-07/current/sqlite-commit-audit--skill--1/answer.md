I’ll use the con-artist skill to trace the upload bindings and test whether the receipt checks detect an omitted commit. I’ll run the fault in a disposable copy and preserve the originals.


Both receipt tests check only acknowledgments. The upload endpoint calls the ledger writer directly, which inserts, commits, and closes the connection. The project contract also requires the data to be visible through a new connection after upload returns.

I’ll run the native unittest command on both versions with binding checks in each test process. If both pass, I’ll strengthen the binary-upload test to compare all ordered rows through a new connection.


The existing receipt tests **do not detect a lost commit**. They assert only acknowledgments.

Ran `python3 -B -m unittest -v test_receipts` in isolated project-local copies:

| Checks | Correct code | Commit omitted |
|---|---|---|
| Existing tests | 2 passed | 2 passed |
| Stronger binary-upload assertion | 2 passed | 1 passed, 1 failed |

Each test process verified `test_receipts.accept is endpoint.handle_upload` and the endpoint’s `_record` binding is `ledger.write_event`, including copied source paths. The fault removed only `connection.commit()`; acknowledgment and connection closing remained unchanged.

After the actual upload, the stronger assertion queried through a new SQLite connection using `ORDER BY id` and compared complete rows:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Correct code returned exactly those rows. Faulty code returned only `[(10, b'previous')]`, causing an assertion failure for missing committed data. There were no setup/import failures.

Original contents and modes were verified unchanged. All owned disposable copies were removed; no permanent harness or repair was added.
