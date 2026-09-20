I’ll inspect the test, endpoint, and ledger, then run the existing tests and a stronger persistence assertion against correct code and an isolated fault that skips the commit.

The receipt tests check only the acknowledgment. Their imported `accept` calls `handle_upload`, which uses the `_record` binding to `write_event`; the ledger commits before closing the connection.

I’ll remove only the commit in a disposable copy. Each test run will verify those bindings in its own process and confirm the ledger writer was reached. The stronger assertion will read all ordered rows through a new connection after the upload.

The existing receipt tests **do not detect a lost commit**.

| Native unittest checks | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Stronger persistence assertion | Passed | Failed: new row missing |

Every run verified, in the same process, that `test_receipts.accept` is `endpoint.handle_upload` and its `_record` binding is `ledger.write_event`. Profiling confirmed that writer was reached.

The stronger assertion called the actual upload, then read complete ordered rows through a new SQLite connection:

- Expected and correct: `[(10, b'previous'), (20, b'\x00\xffnew')]`
- Faulty: `[(10, b'previous')]`

Only the commit was omitted; acknowledgment and connection closing stayed unchanged. Failure was an assertion about missing committed data, with no setup/import errors.

Original bytes and modes were preserved. All owned disposable copies were removed.
