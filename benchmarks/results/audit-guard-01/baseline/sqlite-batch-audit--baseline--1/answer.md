I’ll inspect the contract and tests, then run the audit in disposable project-local copies. I’ll leave the original files unchanged and remove the copies afterward.

The existing tests cover success and empty input, but never exercise a duplicate key. I’ll test a narrow fault that commits each inserted row, then check whether added rollback tests catch it for both a pre-existing key and a duplicate within the batch. Each test process will verify that it loaded its copy-local `batch.py`.

`test_batch.py` **does not protect atomic rollback**. Its unchanged tests pass even when actual `batch.py` is modified to call `connection.commit()` after every insert, allowing partial batches to persist.

Using the supplied interpreter with `-B` and native `unittest`:

| Tests | Implementation | Run | Failures | Exit |
|---|---|---:|---:|---:|
| Existing | Correct | 2 | 0 | 0 |
| Existing | Faulty | 2 | 0 | 0 |
| Strengthened | Correct | 4 | 0 | 0 |
| Strengthened | Faulty | 4 | 2 | 1 |

All runs had zero errors and skips. Native test identities, prefixed by `test_batch.BatchTests.`, were:

- `test_empty` — passed throughout.
- `test_success` — passed throughout.
- `test_duplicate_existing_key_rolls_back` — added in copies; failed only against the fault.
- `test_duplicate_within_batch_rolls_back` — added in copies; failed only against the fault.

Both added tests insert two valid rows before a duplicate. Both successfully observed `sqlite3.IntegrityError`, then failed at the actual rollback assertion:

```python
self.assertEqual(self.records(), before)
```

```text
AssertionError: Lists differ:
[(1, 'seed'), (2, 'two'), (3, 'three')] != [(1, 'seed')]
```

The strengthened test files were byte-identical across implementations. Each executing test process asserted its copy-local implementation path and `test_batch.batch is batch`, then ran the native suite using the real SQLite fixture. These were behavioral failures, not setup failures.

All scratch was removed. Before/after inventory confirmed unchanged original contents, modes, ownership, notes, and Git metadata, including HEAD/index. No original test edits were applied; installed skills were untouched.
