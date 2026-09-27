I’ll use the con-artist skill to trace the receipt tests and upload binding, then compare correct code with an isolated version that omits the ledger commit.


The tests check only acknowledgments. The upload endpoint calls the ledger writer directly, which commits before closing the connection. The project requires committed rows to be visible through a new connection.

I’ll run four native unittest checks in disposable project-local copies: existing tests and a stronger row assertion, each with and without the commit. Each test run will verify the imported endpoint and its writer binding in that same process.


The existing receipt tests **miss the lost commit**: both only assert acknowledgments.

Ran `python3 -B -m unittest -v test_receipts` in four isolated project-local copies:

| Tests | Correct code | Commit omitted |
|---|---|---|
| Existing | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger assertion | 2 passed, exit 0 | 1 failed, exit 1 |

Every run verified, inside the test process, that `test_receipts.accept` was `endpoint.handle_upload`, its `_record` binding was `ledger.write_event`, and both loaded from the intended copy. The fault removed only `connection.commit()`; acknowledgment and closing remained unchanged.

The stronger assertion opened a new SQLite connection after the actual binary upload and compared complete rows ordered by ID:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

Faulty code returned only `[(10, b'previous')]`. The failure therefore detected missing committed data, with no setup/import failure.

Original bytes and modes were verified unchanged. All owned disposable copies were removed; no permanent harness or repair was applied.
