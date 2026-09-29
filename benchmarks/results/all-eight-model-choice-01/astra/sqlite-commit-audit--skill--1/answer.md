I’m using the con-artist skill to trace the receipt tests and upload bindings, then run the commit omission and stronger persistence assertion in disposable project copies.

Both receipt tests check only the acknowledgment. The endpoint calls the ledger writer directly; that writer commits, closes the connection, then returns the acknowledgment. I’ll remove only the commit in the faulty copy and check both bindings inside each native test process. The stronger checks will reopen SQLite after each upload and compare every ordered row, including the existing row and exact payload.

The existing receipt tests **do not detect a lost commit**: they assert only acknowledgment.

Four isolated runs used `python3 -B -m unittest -v test_receipts`:

| Assertions | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed; exit 0 | 2 passed; exit 0 |
| Stronger persistence checks | 2 passed; exit 0 | 2 failed; exit 1 |

Every test process verified both bindings:
- `test_receipts.accept is ingest.endpoint.handle_upload`
- The endpoint’s `_record` binding is `ingest.ledger.write_event`.

The sole production mutation removed `connection.commit()`, preserving acknowledgment and connection closing.

After each actual upload, the stronger checks opened a new SQLite connection and compared complete rows ordered by ID. The binary test expected:
```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```
Faulty code returned only `[(10, b'previous')]`. The empty-payload test likewise failed for its missing new row. Both failures were persistence assertion failures, with no setup/import errors.

Original bytes and modes, including project metadata, were preserved. All owned disposable copies were removed; no permanent changes were made.
