I’ll use the con-artist skill to trace the receipt test’s bindings, run the lost-commit fault in an isolated copy, and check the stronger persistence assertion on both versions.



Both tests check only the acknowledgment. They import the real endpoint, which calls the ledger writer; neither test reads the database afterward. The documented contract requires the exact payload and existing rows to be visible through a new connection.

I’ll remove only `connection.commit()` in a disposable copy, leaving closing and acknowledgment unchanged. Each native test run will verify its imported bindings and trace calls into that copy’s writer in the same process.

The existing receipt tests **do not detect a lost commit**: both assert only the acknowledgment.

Ran `python3 -B -m unittest -v test_receipts` four times in disposable project-local copies:

| Tests | Correct code | Commit omitted |
|---|---|---|
| Existing | 2 passed; exit 0 | 2 passed; exit 0 |
| Stronger assertion | 2 passed; exit 0 | 1 assertion failure; exit 1 |

Every run verified, in the test process, that `test_receipts.accept` was the copied endpoint and its `_record` binding was the copied ledger writer. Profiling confirmed two actual writer calls. The fault omitted only `connection.commit()`; closing and acknowledgment stayed unchanged.

The stronger assertion opened a new SQLite connection after the actual binary upload, queried all rows ordered by ID, and compared:
```python
self.assertEqual(rows, [(10, b'previous'), (20, b'\x00\xffnew')])
```

Faulty code returned only `[(10, b'previous')]`. The failure therefore demonstrated missing committed data, with no setup/import errors.

Original bytes and modes were preserved; all owned disposable copies were removed. No permanent changes were applied.
