I’ll inspect the tests and upload bindings, then run the original and isolated faulty versions with binding checks in the same process. If the existing tests miss the lost commit, I’ll run the stronger SQLite assertion on both versions and remove the disposable copies.

The two receipt tests check only the acknowledgment. The test imports `handle_upload` as `accept`, and the endpoint binds the ledger writer as `_record`. The writer commits before closing the connection and returning the acknowledgment. I’ll remove only that commit in a disposable copy and check both bindings inside each test process.

The existing receipt tests **do not detect a lost commit**.

| Native unittest checks | Correct code | Commit omitted |
|---|---|---|
| Existing receipt tests | 2 passed | 2 passed |
| Stronger persistence assertion | Passed | Failed: missing new row |

Each process verified the actual bindings: `test_receipts.accept is endpoint.handle_upload` and the endpoint’s `_record is ledger.write_event`, plus local module paths.

The fault removed only `connection.commit()`, preserving acknowledgment and connection closing.

The stronger test called the actual imported upload endpoint, then queried complete rows ordered by ID through a new SQLite connection:

- Correct: `[(10, b'previous'), (20, b'\x00\xffnew')]`
- Faulty: `[(10, b'previous')]`

The faulty run failed on that row comparison, not setup or imports. Original bytes and modes were preserved; all owned disposable copies and SQLite scratch were removed.
