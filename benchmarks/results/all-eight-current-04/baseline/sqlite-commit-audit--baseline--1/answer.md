I’ll trace the test’s endpoint and writer bindings, then run the native tests against the original code and an isolated version with only the commit omitted. If both pass, I’ll add the same fresh-connection row assertion to each run and remove the disposable copies afterward.


Both receipt tests check only the acknowledgment. The imported `accept` calls `handle_upload`, which calls the ledger writer through `_record`; the writer commits, closes the connection, and returns the acknowledgment.

I’ll verify those bindings and trace the calls in each test process. For the stronger check, I’ll run each original test and then compare all ordered rows through a new SQLite connection.


The existing receipt tests **do not detect a lost commit**: they assert only the acknowledgment.

| Native unittest checks | Correct code | Commit omitted |
|---|---:|---:|
| Existing receipt tests | 2 passed | 2 passed |
| Added fresh-connection row assertions | 2 passed | 2 failed |

Every test process verified `test_receipts.accept is endpoint.handle_upload` and the endpoint’s `_record is ledger.write_event`. Runtime tracing confirmed both tests reached that endpoint and writer.

The stronger checks ran the original upload tests, then queried `SELECT id, payload FROM events ORDER BY id` through a new connection. For the binary upload:

- Expected: `[(10, b'previous'), (20, b'\x00\xffnew')]`
- Faulty result: `[(10, b'previous')]`

The empty-payload check likewise detected the missing new row. Both failures were data assertion failures, with **zero setup/import errors**.

Only the copied ledger’s commit was removed; acknowledgment and connection closing stayed unchanged. Original bytes and modes were verified unchanged, and all owned disposable copies were removed.
