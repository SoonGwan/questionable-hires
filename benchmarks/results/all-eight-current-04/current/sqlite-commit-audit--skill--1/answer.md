I’ll use the con-artist skill to trace the upload test and bindings, then run the native tests against correct code and an isolated missing-commit fault. I’ll preserve the originals and remove the disposable copies afterward.


The receipt tests only check acknowledgment dictionaries. Their `accept` alias calls the endpoint, whose `_record` binding points directly to the SQLite writer. The writer commits before closing the connection, so omitting only `commit()` should leave acknowledgments intact while losing the new row.

I’ll check both bindings inside each native test run, then add the same fresh-connection row assertion to both isolated versions.


The existing receipt tests **do not detect a lost commit**. They assert acknowledgment only.

Ran `python3 -B -m unittest -v test_receipts` in isolated project-local copies:

| Assertions | Correct code | Commit omitted |
|---|---|---|
| Existing receipt checks | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger persistence checks | 2 passed, exit 0 | 2 failed, exit 1 |

Every run verified, within the native test process, that `test_receipts.accept is endpoint.handle_upload` and `endpoint._record is ledger.write_event`, including their copied source paths and commit presence.

The fault omitted only `connection.commit()`; acknowledgment and connection closing stayed unchanged.

The stronger checks opened a new SQLite connection after each actual upload and compared complete rows ordered by ID. Correct code returned the previous row plus the exact binary payload `(20, b'\x00\xffnew')` or empty payload `(30, b'')`. Faulty code returned only `[(10, b'previous')]`. Both failures were missing-data assertions, with no setup/import errors.

Original bytes and modes were preserved. All owned disposable copies were removed; no harness or report remains.
