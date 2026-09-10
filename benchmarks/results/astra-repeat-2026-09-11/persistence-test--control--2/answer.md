I’ll inspect the test and write path, run an isolated lost-write mutation, and verify that production code remains unchanged.

The test misses the lost write: it still passes when `store.append(record)` is removed in memory because it only checks the success flag. I’ll add an assertion for the stored record and rerun the same mutation.

The original test **missed a lost write**: removing `store.append(record)` in an isolated, in-memory mutation still passed.

Updated `test_service.py` to assert that the store contains the record.

Verified:
- Production implementation passes.
- Mutated implementation fails with `[] != ['record']`.
- `git diff --check` passes.

Production code remains unchanged; no deliberate fault was left behind.
