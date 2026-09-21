I’ll use the con-artist skill to trace the atomicity assertions, run the four comparisons in disposable project-local copies, and verify which implementation each test process executes. I’ll leave the originals unchanged and remove the copies afterward.

The existing tests check successful writes and empty input, but never exercise a duplicate key. I’ll add a per-row commit fault in copied `batch.py`; it should preserve those controls while allowing a partial batch to persist. The proposed tests will check both a duplicate of an existing row and a duplicate within the batch, asserting `IntegrityError` and exact database contents afterward.

`test_batch.py` does **not protect atomic rollback**. Adding `connection.commit()` after each INSERT in copied `batch.py` allowed partial writes while both existing tests still passed.

Used the supplied interpreter with `-B`, invoking native `unittest.main(module=None, argv=["unittest", "-v", "test_batch"])`.

| Tests | Implementation | Native result | Exit |
|---|---|---|---|
| Existing | Correct | 2 passed | 0 |
| Existing | Per-row commit fault | 2 passed | 0 |
| Strengthened | Correct | 4 passed | 0 |
| Strengthened | Same fault | 2 passed, 2 failed | 1 |

Native identities, all under `test_batch.BatchTests`:

- `test_success`
- `test_empty`
- `test_duplicate_existing_rolls_back` — proposed
- `test_duplicate_within_batch_rolls_back` — proposed

The identical strengthened tests retained both controls. Each added test captured the initial records, asserted `sqlite3.IntegrityError`, then asserted `self.assertEqual(self.records(), before)`. Exception assertions passed; the faulty implementation failed the database assertions:

```text
test_duplicate_existing_rolls_back:
[(1, 'seed'), (2, 'two')] != [(1, 'seed')]

test_duplicate_within_batch_rolls_back:
[(1, 'seed'), (2, 'two'), (3, 'three')] != [(1, 'seed')]
```

In-process tracing verified every actual `append_batch` call’s copy-local code path, module binding, and source hash. These were real SQLite executions using the unchanged fixture; there were no setup errors or simulated implementations.

All scratch was removed. Whole-project before/after checks confirmed identical file contents, paths, and modes, including owner notes, skill resources, and Git metadata. No test edits or production fixes were applied.
