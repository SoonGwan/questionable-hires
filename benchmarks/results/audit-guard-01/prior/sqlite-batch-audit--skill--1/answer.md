I’ll use the con-artist skill to check the contract and assertions, then run the correct and faulty implementations in disposable project-local copies. I’ll verify which implementation each test process executes and remove all scratch files afterward.


The existing tests check successful inserts and empty input, but never trigger a duplicate key. I’ll add one fault in the copied `batch.py`: committing after each insert. Then I’ll verify rollback assertions for both a duplicate of an existing row and a duplicate within the incoming batch, keeping both existing controls unchanged.


`test_batch.py` does **not protect atomic rollback**. Both existing tests pass when copied `batch.py` is changed to commit after every insert, allowing partial batches to persist.

Using the supplied interpreter with `-B` and native `unittest -v test_batch` dispatch:

| Tests | Implementation | Count | Result | Exit |
|---|---|---:|---|---:|
| Existing | Correct | 2 | Pass | 0 |
| Existing | Faulty | 2 | Pass | 0 |
| Strengthened | Correct | 4 | Pass | 0 |
| Strengthened | Faulty | 4 | 2 assertion failures | 1 |

Native identities, all under `test_batch.BatchTests`:

- `test_success` — passed throughout.
- `test_empty` — passed throughout.
- `test_duplicate_existing_rolls_back` — added in copies.
- `test_duplicate_within_batch_rolls_back` — added in copies.

Both added tests insert a valid row before encountering a duplicate, assert `sqlite3.IntegrityError`, then compare persisted records with the pre-call snapshot. Exception assertions passed; both faulty-code failures were:

```python
self.assertEqual(self.records(), before)
AssertionError: Lists differ: [(1, 'seed'), (2, 'two')] != [(1, 'seed')]
```

The strengthened test files were byte-identical across implementations. In-process call tracing verified each executing function’s source path, module path, and binding through `test_batch.batch` matched its copy-local `batch.py`. Tests used the unchanged real SQLite fixture; there were no setup errors.

All scratch was removed. Original contents, modes, ownership, owner notes, Git HEAD/index, and skill resources remained unchanged. No test edits were applied.
