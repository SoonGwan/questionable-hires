I’ll use the con-artist skill to trace the receipt test, verify its runtime bindings, and compare correct code with an isolated missing-commit fault. I’ll preserve the originals and remove the disposable copies afterward.


Both receipt tests assert only the acknowledgment. The endpoint calls the ledger through `_record`; the ledger commits the insert and closes the connection in `finally`. I’ll remove only the commit in the disposable fault copy, then check persistence by reading all ordered rows through a new connection after the existing binary-upload test’s call.


The existing receipt tests **miss the lost commit**: both pass when only `connection.commit()` is removed, leaving acknowledgment and connection closing unchanged.

Verified in all four check processes that the actual tests’ `accept` is `endpoint.handle_upload`, and that endpoint’s `_record` is `ledger.write_event`.

| Native unittest check | Correct code | Missing commit |
|---|---|---|
| Existing receipt tests | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger persistence assertion | Passed, exit 0 | AssertionError, exit 1 |

The stronger test executes the existing binary-upload test, opens a new SQLite connection, and compares the complete rows ordered by ID:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Faulty code returns only `[(10, b'previous')]`. The failure is missing committed data, with no setup or import failure.

Commands and results were captured through the skill’s audit helper. Original bytes and modes were preserved; all owned disposable copies were removed.
