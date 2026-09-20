I’ll use the con-artist skill to trace the receipt tests and bindings, then run the existing and stronger checks against correct code and an isolated missing-commit fault. I’ll preserve the originals and remove the disposable copies.


The two receipt tests check only acknowledgments. Their imported `accept` points to `handle_upload`, which calls the ledger writer through `_record`. The writer commits before closing the connection.

I’ll remove only that commit in the faulty copy, verify both bindings and actual calls inside each test process, and check persisted rows through a new connection after each original test’s upload.


The existing receipt tests **miss the lost commit**: both check acknowledgment only.

Executed with native `unittest` in disposable project-local copies:

| Checks | Correct code | Commit omitted |
|---|---|---|
| Existing tests | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger assertions | 2 passed, exit 0 | 2 failed, exit 1 |

Each test process verified `test_receipts.accept is endpoint.handle_upload` and its `_record` binding to `ledger.write_event`, and traced two actual calls through both functions.

The stronger checks ran the original upload tests, then read `SELECT id, payload FROM events ORDER BY id` through a new SQLite connection. Correct code returned the complete expected rows, including `(10, b'previous')` and exact binary payload `(20, b'\x00\xffnew')`. Faulty code returned only the pre-existing row. Both failures specifically reported missing committed data; there were no setup/import errors.

Only the commit was omitted; acknowledgment and connection closing stayed unchanged. Original bytes/modes were preserved, and all owned disposable copies were removed.
