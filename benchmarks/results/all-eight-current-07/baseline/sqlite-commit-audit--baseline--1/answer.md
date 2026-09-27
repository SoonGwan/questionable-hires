I’ll inspect the test and upload-to-ledger bindings, then run the native tests and the stronger persistence check on the original code and an isolated copy with the commit omitted.

The two receipt tests assert only the acknowledgment. Their imported `accept` is `handle_upload`, which calls the bound ledger writer `_record`.

I’ll verify those identities and file origins in each test process. The stronger check will run the original binary-upload test, then open a new SQLite connection and compare all ordered rows, including the pre-existing row and exact binary payload.

The existing receipt tests **do not detect a lost commit**: both check acknowledgments only.

| Native unittest check | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Stronger persistence assertion | Passed | Failed: missing committed data |

In each test process, verified `test_receipts.accept is endpoint.handle_upload` and `endpoint._record is ledger.write_event`, including file origins. Runtime tracing confirmed the writer was reached and connections closed. The fault removed only `connection.commit()`; acknowledgment and closing remained unchanged.

The stronger assertion executed the actual binary-upload test, then read complete ordered rows through a new SQLite connection:

- Correct: `[(10, b'previous'), (20, b'\x00\xffnew')]`
- Faulty: `[(10, b'previous')]`

The failure was an assertion about missing data, with no setup/import errors. Original bytes and modes were preserved; all owned disposable copies were removed.
