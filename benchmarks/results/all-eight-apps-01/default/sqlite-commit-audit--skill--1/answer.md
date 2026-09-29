I’ll use the con-artist skill to trace the receipt tests and upload bindings, then run the native checks against correct code and an isolated commit-omission fault. I’ll preserve the originals and remove the disposable copies afterward.


The two receipt tests check only acknowledgment dictionaries. The contract also requires rows to be visible through a new SQLite connection after upload returns. The endpoint calls the ledger writer directly, so omitting its commit should leave acknowledgments intact while losing the new row.

I’ll run all four checks with binding verification inside each native test process and trace the upload and writer calls to confirm the fault is reached.


The existing receipt tests **do not detect a lost commit**: both assert only acknowledgments.

Ran `python3 -B -m unittest -v test_receipts` in isolated project-local copies:

| Assertions | Correct code | Commit omitted |
|---|---|---|
| Existing tests | 2 pass, exit 0 | 2 pass, exit 0 |
| Stronger tests | 2 pass, exit 0 | 1 assertion failure, exit 1 |

Every test process verified `test_receipts.accept is endpoint.handle_upload` and the endpoint’s `_record is ledger.write_event`, including copied source paths. Tracing confirmed two actual upload-to-writer calls per run.

The stronger binary test opened a new SQLite connection after the actual upload and compared complete rows ordered by ID:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Correct code returned exactly those rows. Faulty code returned only `[(10, b'previous')]`, failing specifically for missing committed data. Acknowledgment and connection closing remained unchanged.

Original file bytes and modes were preserved. All owned disposable copies were removed; no permanent changes remain.
