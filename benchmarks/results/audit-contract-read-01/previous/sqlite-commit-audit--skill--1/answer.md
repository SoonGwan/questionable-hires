I’ll use the con-artist skill to trace the receipt tests and upload binding, then compare correct code with an isolated omitted-commit fault using native tests and a persisted-data assertion.

Both receipt tests check only acknowledgment dictionaries. The upload endpoint calls the ledger writer directly; that writer inserts, commits, closes the connection, then acknowledges. The project contract requires exact rows to be visible through a new connection.

I’ll run all four checks with `python3 -B -m unittest`, verifying the test’s endpoint import and the endpoint’s writer binding inside each test process. The fault will remove only the writer’s commit; the stronger assertion will compare every ordered row after the binary upload.

The existing receipt tests **do not detect a lost commit**: both check only acknowledgment dictionaries.

Four isolated runs used `python3 -B -m unittest -v test_receipts`:

| Checks | Correct code | Commit omitted |
|---|---|---|
| Existing tests | 2 passed | 2 passed |
| Stronger assertion | 2 passed | 1 failed, 1 passed |

Every run verified, within the test process, that the actual test’s `accept` imports `endpoint.handle_upload` and that endpoint’s `_record` binds to the copied `ledger.write_event`.

The fault removed only `connection.commit()`, preserving acknowledgment and connection closing. After the actual binary upload, the stronger assertion opened a new SQLite connection and compared complete ordered rows:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Faulty code returned only `[(10, b'previous')]`. The failure was missing committed data, with no setup or import errors.

Original file bytes and modes were preserved; all owned disposable copies were removed.
