I’ll inspect the test, endpoint, and ledger bindings, then run the native tests against the original code and an isolated commit-omission fault. If they miss it, I’ll run the stronger persistence assertion on both versions.


Both existing tests check only the acknowledgment. The upload endpoint’s writer commits before closing its connection; I’ll remove only that commit in a disposable copy and verify the actual test’s endpoint and writer bindings in each test process.


The existing receipt tests **do not detect a lost commit**: both check only acknowledgments.

| Native `unittest` checks | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Stronger persistence assertion | Passed | Failed: missing new row |

Every test process verified `test_receipts.accept is endpoint.handle_upload` and `endpoint._record is ledger.write_event`. Execution tracing confirmed that the bound writer was reached.

The identical stronger assertion read all ordered rows through a new SQLite connection after the actual upload:

- Expected and observed on correct code: `[(10, b'previous'), (20, b'\x00\xffnew')]`
- Observed on faulty code: `[(10, b'previous')]`

The faulty run produced one assertion failure and zero errors—not an import or setup failure. Only `connection.commit()` was removed; acknowledgment and connection closing remained unchanged.

Original bytes and modes were preserved. Owned disposable copies were removed.
