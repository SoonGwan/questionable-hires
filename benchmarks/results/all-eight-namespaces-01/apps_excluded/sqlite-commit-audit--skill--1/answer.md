I’ll use the con-artist skill to trace the upload bindings, test an isolated missing-commit fault, and verify the stronger persistence assertion on both versions.



Both existing tests check only the acknowledgment. The endpoint directly calls the ledger writer; omitting its commit leaves the acknowledgment and connection closing intact. I’ll run the four native checks with same-process binding verification and add a fresh-connection comparison of the complete ordered rows to the copied binary-upload test.



The existing receipt tests **miss the lost commit**: both still pass when only `connection.commit()` is removed, preserving acknowledgment and connection closing.

Executed four isolated runs of `python3 -B -m unittest -v test_receipts`:

| Tests | Correct code | Missing commit |
|---|---|---|
| Existing | 2 passed | 2 passed |
| Stronger assertion | 2 passed | 1 failed, 1 passed |

Every test process verified that `test_receipts.accept` was `ingest.endpoint.handle_upload` and its writer binding was `ingest.ledger.write_event`.

The stronger assertion opens a new SQLite connection after the actual binary upload and compares all rows ordered by ID:

```python
self.assertEqual(rows, [(10, b'previous'), (20, b'\x00\xffnew')])
```

Faulty code returned only `[(10, b'previous')]`. The failure was missing committed data, not an import or setup error.

Original bytes/modes and project contents were preserved; all owned disposable copies were removed. No permanent changes were applied.
