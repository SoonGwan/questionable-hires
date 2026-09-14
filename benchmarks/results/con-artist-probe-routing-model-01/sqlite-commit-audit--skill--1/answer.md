I’m using the con-artist skill to trace the receipt tests and run the lost-commit fault in an isolated copy, with binding checks inside each test process.

Both receipt tests assert only the acknowledgment. Their imported `accept` calls the endpoint’s `_record` binding, which inserts, commits, and closes the SQLite connection. I’ll omit only `commit()` and, if the tests stay green, check the complete persisted rows through a new connection using the same native fixture.

The existing receipt tests **miss the lost commit**. Removing only `connection.commit()` leaves acknowledgment and connection closing unchanged.

| Native unittest check | Correct code | Missing commit |
|---|---|---|
| Existing receipt tests | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger persistence assertion | 1 passed, exit 0 | 1 failed, exit 1 |

Every check process verified the actual test binding: `accept → endpoint.handle_upload → ledger.write_event`, with imports resolving inside its disposable copy.

The stronger test executed the actual binary receipt test, then queried through a new SQLite connection using `ORDER BY id` and compared complete rows:

```python
expected = [(10, b'previous'), (20, b'\x00\xffnew')]
# Faulty code returned:
actual = [(10, b'previous')]
```

The failure was missing committed data, with no setup/import failure. This persistence assertion closes the demonstrated gap.

All five selected original files retained their bytes and modes. Owned disposable copies were removed; no harness or report was retained.
