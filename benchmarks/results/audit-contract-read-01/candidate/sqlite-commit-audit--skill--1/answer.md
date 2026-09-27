I’ll use the con-artist skill to trace the receipt tests and upload bindings, then compare correct code with an isolated omitted-commit fault using the same native checks.

Both receipt tests check only the acknowledgment. The imported upload endpoint calls the ledger writer directly, and the ledger commits before closing the connection.

I’ll verify those bindings inside each native test run and trace execution through the writer. If the omitted-commit fault survives, I’ll add a fresh-connection check for all ordered rows, including the pre-existing row and exact uploaded bytes.

The existing receipt tests **do not detect a lost commit**: they assert only acknowledgment.

Executed four isolated runs with `python3 -B -m unittest -v test_receipts`:

| Assertions | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Added fresh-connection row checks | 2 passed | 2 failed |

Every run verified, in the test process, that `test_receipts.accept` was the copied endpoint and its `_record` binding was the copied ledger writer. Execution tracing confirmed the faulty writer still closed the connection and returned acknowledgment.

The stronger checks queried `SELECT id, payload FROM events ORDER BY id` through a new connection after upload. The binary check expected:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Faulty code returned only `[(10, b'previous')]`. The empty-payload check likewise failed for missing committed data. Neither failure involved setup or imports.

Original file bytes and modes were preserved; all owned disposable copies were removed.
