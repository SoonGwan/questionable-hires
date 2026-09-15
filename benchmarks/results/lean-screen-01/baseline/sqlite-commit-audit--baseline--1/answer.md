I’ll inspect the tests, endpoint, and ledger, then run the native checks against the original code and an isolated copy with the commit omitted. I’ll verify the bindings within each test process and remove the disposable copy afterward.


The two receipt tests check only the acknowledgment. The endpoint delegates to the imported ledger writer, which inserts, commits, closes the connection, and returns the acknowledgment. I’ll remove only the commit in a disposable copy and run both test sets with in-process binding checks and a trace confirming the writer is reached.


**The existing receipt tests do not detect a lost commit.** Both assert only the acknowledgment.

| Checks | Correct code | Commit omitted |
|---|---|---|
| Existing native tests | 2 passed | 2 passed |
| Stronger native assertion | Passed | Failed: missing committed row |

Every test process verified `test_receipts.accept is endpoint.handle_upload` and the endpoint’s `_record is ledger.write_event`. Execution traces confirmed the writer was reached, closed the connection, and returned the acknowledgment on both versions.

The identical stronger assertion queried a **new SQLite connection after upload**, comparing complete rows ordered by ID:

- Correct: `[(10, b'previous'), (20, b'\x00\xffnew')]`
- Faulty: `[(10, b'previous')]`

The fault failed specifically for missing committed data, with no setup/import errors.

Original bytes and modes were verified unchanged. Owned disposable copies were removed; no harness or report remains.
