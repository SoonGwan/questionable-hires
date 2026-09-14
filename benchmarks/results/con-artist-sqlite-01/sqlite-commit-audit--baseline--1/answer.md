I’ll inspect the test and upload bindings, then run the native tests and a stronger persistence check against the original code and an isolated fault copy.

The existing tests check only acknowledgments. The test’s `accept` alias points to `handle_upload`, which calls the ledger writer through `_record`. The writer commits before closing the connection.

I’ll verify those bindings in each test process and remove only the commit statement in the fault copy. The stronger check will compare all ordered rows through a fresh SQLite connection after the upload returns.

The existing receipt tests **do not detect a lost commit**.

| Native unittest check | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Stronger persistence assertion | Passed | Failed: new row missing |

Each test process verified the actual binding chain: `test_receipts.accept → endpoint.handle_upload → ledger.write_event`, including source paths.

The isolated fault removed only `connection.commit()`; acknowledgment and connection closing stayed unchanged.

After the actual upload, the stronger assertion read complete ordered rows through a new SQLite connection:

- Correct: `[(10, b'previous'), (20, b'\x00\xffnew')]`
- Faulty: `[(10, b'previous')]`

The faulty run failed on missing committed data, with no setup/import errors. Original bytes and modes were preserved, and all owned disposable copies were removed.
