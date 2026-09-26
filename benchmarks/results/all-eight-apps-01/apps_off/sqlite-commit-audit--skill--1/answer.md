I’ll use the con-artist skill to trace the receipt tests and upload bindings, then run the four checks in disposable project copies with same-process binding verification. I’ll preserve the originals and remove the copies afterward.


Both receipt tests check only the acknowledgment. The endpoint calls the ledger writer, which inserts, commits, closes the connection, and returns that acknowledgment. The stated contract also requires the exact rows to be visible through a new connection.

I’ll omit only `connection.commit()` in the faulty copy. Each native test process will verify its imported endpoint and writer binding and record that the writer was reached. If the tests survive, I’ll add the same complete-row assertions to both copies.


The existing receipt tests **do not detect a lost commit**. They assert only acknowledgment; omitting the ledger’s commit leaves both tests passing.

Executed four isolated runs using `python3 -B -m unittest -v test_receipts`:

| Assertions | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger persistence assertions | 2 passed, exit 0 | 2 failed, exit 1 |

Every test process verified `test_receipts.accept` → `endpoint.handle_upload` → `ledger.write_event`, including copied source paths. Runtime instrumentation confirmed two endpoint and two writer calls per run.

The stronger assertions opened a new SQLite connection after each upload and compared complete rows ordered by ID. The binary test expected `[(10, b'previous'), (20, b'\x00\xffnew')]`; faulty code returned only `[(10, b'previous')]`. The empty-payload test likewise failed for missing committed data. Neither failure involved setup or imports.

Acknowledgment and connection closing remained unchanged. All disposable copies were removed; original file bytes, modes, and inventory were verified unchanged.
