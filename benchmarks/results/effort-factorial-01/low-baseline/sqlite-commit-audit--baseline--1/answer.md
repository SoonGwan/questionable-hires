I’ll inspect the receipt tests and upload bindings, then run them against the original code and an isolated copy with the ledger commit omitted. If they miss the fault, I’ll test both versions with a fresh-connection row comparison.


The two existing tests check only acknowledgments. Their imported `accept` function is `ingest.endpoint.handle_upload`, which calls the ledger writer through `_record`. The writer commits, closes the connection, then returns the acknowledgment. I’ll remove only the commit in a disposable copy and verify those bindings in each test process.


The existing receipt tests **do not detect a lost commit**.

| Native tests | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Stronger durability assertion | Passed | Failed: missing new row |

In each test process, verified:
- `test_receipts.accept is endpoint.handle_upload`
- The endpoint’s `_record` binding is `ledger.write_event`
- Both existing uploads actually reached that writer.

The fault removed only `connection.commit()`; acknowledgment and connection closing stayed unchanged.

After the actual binary upload, the stronger assertion opened a new SQLite connection and compared complete rows ordered by ID:

```python
# Correct:
[(10, b'previous'), (20, b'\x00\xffnew')]

# Faulty:
[(10, b'previous')]
```

The faulty run failed on missing committed data, with no setup or import errors. Original bytes and modes were preserved; all owned disposable copies were removed.
