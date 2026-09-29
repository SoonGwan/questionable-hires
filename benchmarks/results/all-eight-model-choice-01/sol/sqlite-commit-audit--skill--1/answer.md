I’m using the con-artist skill to trace the receipt test through the upload endpoint and ledger writer, then run the native test against correct code and an isolated commit omission. I’ll check the endpoint binding inside the test process and keep the project files unchanged.

The existing tests assert only the acknowledgment. The upload endpoint binds the ledger writer, and the ledger commits before closing; removing that commit should leave the acknowledgment intact while SQLite rolls back the insert. The first baseline command used `python`, which is unavailable here, so I’m using the project’s documented `python3 -B -m unittest` runner for the controlled checks.

The existing receipt tests **miss a lost commit**. In disposable copies, I removed only `connection.commit()` from the ledger writer, leaving the acknowledgment and connection closing intact.

Using `python3 -B -m unittest -v test_receipts`, the existing tests passed on both correct code and the faulty copy (2/2 each). A binding check in each test process verified that the test’s `accept` name resolved to `endpoint.handle_upload` and that the endpoint used the copied `ledger.write_event`.

I then ran the same stronger native test on both versions. After the actual upload call, it opened a new SQLite connection and compared all ordered rows with `[(10, b'previous'), (20, b'\x00\xffnew')]`. Correct code passed (3/3); the faulty copy failed that assertion because it returned only `[(10, b'previous')]`.

Original file bytes and modes were unchanged, and the disposable copies were removed.
