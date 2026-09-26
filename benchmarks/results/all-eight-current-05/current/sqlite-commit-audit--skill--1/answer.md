I’ll use the con-artist skill to trace the receipt tests and run the commit-omission audit in disposable project copies, verifying bindings in each test process.



Both tests check only the acknowledgment. The endpoint calls the real ledger writer, which commits before closing. I’ll remove only that commit in a copy, then check whether assertions reading all ordered rows through a fresh connection detect the loss while preserving the seeded row and exact payload.



The existing receipt tests **miss the lost commit**: both assert only acknowledgment.

Ran `python3 -B -m unittest -v test_receipts` in four disposable project-local copies:

| Assertions | Correct code | Commit omitted |
|---|---|---|
| Existing tests | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger persistence checks | 2 passed, exit 0 | 2 failed, exit 1 |

Each test process verified `accept → handle_upload → _record → write_event`, including copied source paths. Execution tracing confirmed two endpoint and two writer calls per run. The fault omitted only `connection.commit()`; acknowledgment and closing stayed unchanged.

The stronger checks opened a new SQLite connection after each upload and compared complete rows ordered by ID. Correct binary-upload output was:
```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```
Faulty output was:
```python
[(10, b'previous')]
```
The empty-payload check likewise detected its missing row. Both failures were missing-data assertions, with no setup/import errors.

All owned copies were removed. Original file bytes and modes were verified unchanged; no permanent harness or repair was applied.
