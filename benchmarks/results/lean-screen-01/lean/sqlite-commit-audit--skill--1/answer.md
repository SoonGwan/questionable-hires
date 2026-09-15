I’ll use the con-artist skill to trace the upload test and writer binding, then run the native tests and a stronger persistence check on correct and isolated faulty code. I’ll preserve the originals and remove the disposable copies.

The two receipt tests only check acknowledgments. The endpoint’s `_record` binding points to the ledger writer, which commits before closing the connection. I’ll omit only that commit in the faulty copy and verify both bindings inside each test process. If the tests still pass, I’ll add a check that reads all ordered rows through a new connection after the upload.

**The existing receipt tests miss the lost commit.** Both check only acknowledgments.

| Native unittest checks | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Existing tests + persistence assertion | 3 passed | 2 passed, 1 failed |

Every test process verified `test_receipts.accept is endpoint.handle_upload` and the endpoint’s `_record is ledger.write_event`. Call tracing confirmed both functions executed.

The identical stronger assertion opened a new SQLite connection after the actual upload and compared complete rows ordered by ID:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Faulty code returned only `[(10, b'previous')]`. The failure demonstrated missing committed data, with no setup/import failure. Acknowledgment and connection closing remained unchanged.

Original file bytes and modes were verified unchanged; all owned disposable copies were removed.
