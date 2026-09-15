I’m using the con-artist skill to trace the receipt test’s bindings, run an isolated commit-omission fault, and verify a stronger persistence assertion against both versions.

Both tests assert only the acknowledgment. The endpoint binds directly to `ledger.write_event`, which inserts, commits, closes, and then acknowledges. I’ll omit only the commit in a disposable copy and check the bindings and executed calls inside each native test process.

**The existing receipt tests miss the lost commit.** They assert acknowledgment only.

Ran `python3 -B -m unittest -v test_receipts` in four isolated project-local copies:

| Assertions | Correct code | Commit omitted |
|---|---|---|
| Existing | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger persistence checks | 2 passed, exit 0 | 2 failures, exit 1 |

Each test process verified `accept is endpoint.handle_upload` and its `_record is ledger.write_event`, checked copied source paths, and recorded two calls to each function. The fault omitted only `connection.commit()`; acknowledgment and closing stayed unchanged.

The stronger checks opened a new SQLite connection after each actual upload and compared complete rows ordered by ID, including the pre-existing row and exact binary/empty payload. Faulty code returned only `[(10, b'previous')]`. Both failures were missing-data assertions; no setup/import errors occurred.

Original bytes and modes were preserved. All owned disposable copies were removed; no permanent changes were made.
