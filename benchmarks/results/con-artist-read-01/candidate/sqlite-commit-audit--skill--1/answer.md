I’ll use the con-artist skill to trace the receipt tests and upload bindings, then run the existing and stronger checks against correct code and an isolated missing-commit fault.



Both existing tests check only the acknowledgment. The upload endpoint delegates to the ledger writer, which commits before closing the connection; omitting that commit should still return the expected acknowledgment while losing the insert.

I’ll verify both bindings inside each test process, then add the same fresh-connection row assertion to both disposable versions.



The existing receipt tests **do not detect a lost commit**. Both assert only acknowledgment responses.

Ran `python3 -B -m unittest -v audit_probe` in disposable project-local copies. The probe loaded the actual receipt tests and verified, in every test process:

- `test_receipts.accept is endpoint.handle_upload`
- The endpoint’s `_record is ledger.write_event`
- Both uploads reached that writer.

The fault removed only `connection.commit()`, preserving acknowledgment and connection closing.

| Tests | Correct code | Missing commit |
|---|---|---|
| Existing | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger | 2 passed, exit 0 | 1 assertion failure, exit 1 |

The identical stronger check opened a new SQLite connection after the actual binary upload, queried all rows with `ORDER BY id`, and asserted:

```python
self.assertEqual(rows, [(10, b'previous'), (20, b'\x00\xffnew')])
```

Faulty code returned only `[(10, b'previous')]`: failure was specifically missing committed data, with no setup/import errors.

Original file bytes and modes were preserved. All owned disposable copies were removed; no permanent changes were made.
