I’ll use the con-artist skill to trace the receipt test and its bindings, then run the existing and stronger checks against isolated correct and missing-commit versions. I’ll preserve the originals and remove the disposable copies afterward.


The two receipt tests check only acknowledgments. The endpoint calls the ledger writer directly, and closing its connection without committing would discard the insert while still returning the expected acknowledgment.

I’ll run all four checks with binding verification inside each test process. The stronger check will read from a new SQLite connection after the binary upload and compare both complete rows in ID order.


The existing receipt tests **miss the lost commit**: both check only acknowledgments.

All four runs used `python3 -B -m unittest -v test_receipts` in disposable project-local copies:

| Tests | Correct code | Commit omitted |
|---|---|---|
| Existing | 2 passed, exit 0 | 2 passed, exit 0 |
| Stronger assertion | 2 passed, exit 0 | 1 failed, exit 1 |

Every test process verified `test_receipts.accept is endpoint.handle_upload` and the endpoint’s writer binding to `ledger.write_event`. Runtime tracing confirmed both functions were reached twice per run.

The stronger assertion opened a new SQLite connection after the actual binary upload and compared complete rows ordered by ID:

```python
[(10, b'previous'), (20, b'\x00\xffnew')]
```

The faulty version returned only `[(10, b'previous')]`. It failed specifically for missing committed data; acknowledgment and connection closing remained unchanged.

Original bytes and modes were preserved. All owned disposable copies were removed.
