I’ll inspect the tests and upload bindings, then run the existing tests and a persistence assertion against correct code and an isolated copy with the commit omitted. I’ll preserve the originals and remove the disposable copy.

Both existing tests check only the acknowledgment. The test’s `accept` import points to `handle_upload`, which calls the ledger writer through `_record`; that writer commits before closing the connection.

I’ll verify those bindings inside each test process and confirm the faulty writer is reached. The stronger check will call the same `accept`, open a new SQLite connection, and compare all rows in ID order, including the previous row and exact binary payload.

The existing receipt tests **do not detect a lost commit**: both check only acknowledgments.

| Native unittest checks | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 pass | 2 pass |
| Stronger persistence assertion | Pass | Fails: missing new row |

Every check process verified `test_receipts.accept is endpoint.handle_upload` and the endpoint’s `_record is ledger.write_event`, including module paths. Execution tracing confirmed the commit/omission line was reached.

The identical stronger assertion called the actual upload, opened a new SQLite connection, and compared complete rows ordered by ID:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Faulty code returned only `[(10, b'previous')]`. Failure was an assertion about missing committed data, with no setup/import errors.

Only the disposable copy’s commit was omitted; acknowledgment and connection closing stayed unchanged. Original bytes/modes were preserved, disposable files removed, and Git status is clean.
