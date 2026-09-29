I’ll use the con-artist skill to trace the receipt test’s bindings and run the four checks in disposable project copies, leaving the originals unchanged.

Both tests check only the acknowledgment dictionary. The endpoint calls the ledger writer, which commits before closing; omitting that commit should still return the acknowledgment while losing the inserted row. I’ll verify both bindings inside each native test process, then check persistence through a fresh SQLite connection.

The existing receipt tests **do not detect a lost commit**: they assert only acknowledgments.

Executed four native runs using `python3 -B -m unittest -v test_receipts`:

| Tests | Correct code | Commit omitted |
|---|---|---|
| Existing | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger | 2 passed, exit 0 | 2 assertion failures, exit 1 |

Each test process verified `test_receipts.accept` was the copied endpoint and its `_record` binding was the copied ledger writer. Tracing confirmed actual writer execution, with acknowledgment and connection closing unchanged.

The stronger checks opened a new SQLite connection after each actual upload and compared complete rows ordered by ID. For binary upload:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Correct code returned exactly these rows. Faulty code returned only `[(10, b'previous')]`; both stronger tests failed for missing committed data, with no setup/import errors.

All disposable copies were removed. Original file bytes and modes were verified unchanged; no permanent harness or changes remain.
