I’ll trace the receipt test, endpoint, and ledger writer, then run the existing tests and a persistence check on correct code and an isolated copy with the commit omitted. I’ll verify the bindings in each test process and remove the disposable copies afterward.


The receipt tests check only the acknowledgment. The imported endpoint calls `_record`, which is bound to `ingest.ledger.write_event`; that writer commits before closing the connection. I’ll omit only the commit in the faulty copy, then check whether both receipt tests still pass and whether a new connection can read the uploaded bytes.


The existing receipt tests **do not detect a lost commit**. They assert only the acknowledgment.

| Native unittest check | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Stronger persistence assertion | Passed | Failed: uploaded row missing |

In every test process, verified `test_receipts.accept is endpoint.handle_upload` and that its `_record` binding is `ledger.write_event`. Execution tracing confirmed the faulty writer was reached, closed its connection, and returned the unchanged acknowledgment.

The identical stronger assertion called the actual imported upload endpoint, then read all rows through a **new SQLite connection**, ordered by ID:

- Expected and correct: `[(10, b'previous'), (20, b'\x00\xffnew')]`
- Faulty: `[(10, b'previous')]`

The failure was a row-comparison assertion for missing committed data; setup and imports succeeded.

Original bytes and modes were preserved. All owned disposable copies were removed.
