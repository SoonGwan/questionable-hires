I’ll use the con-artist skill to trace the receipt tests and bindings, then run the original and stronger checks against correct code and an isolated missing-commit fault.

Both receipt tests assert only the acknowledgment. The endpoint directly calls the ledger writer, which commits before closing the connection. I’ll remove only `connection.commit()` in the disposable fault copy, then check whether the existing tests notice and whether a fresh-connection row assertion catches the loss.

The existing receipt tests **do not detect a lost commit**. They check only acknowledgment.

Verified inside all four native test processes that both actual test methods’ `accept` binding resolves to `endpoint.handle_upload`, whose `_record` binding resolves to `ledger.write_event`.

Each run used `python3 -B -m unittest -v test_receipts`:

| Assertions | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed; exit 0 | 2 passed; exit 0 |
| Stronger persistence assertions | 2 passed; exit 0 | 2 failed; exit 1 |

The isolated fault removed only `connection.commit()`, preserving acknowledgment and connection closing.

The stronger checks opened a new SQLite connection after each actual upload and compared complete rows ordered by ID. The faulty binary-upload result was:

```python
actual:   [(10, b'previous')]
expected: [(10, b'previous'), (20, b'\x00\xffnew')]
```

The empty-upload check likewise failed for its missing new row. Both failures were assertion failures for missing committed data, with successful imports and setup.

Original bytes and modes were preserved, the project inventory remained unchanged, and all owned disposable copies were removed.
