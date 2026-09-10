I’ll inspect the test and write path, then run an isolated lost-write mutation to see whether the test detects it.

The test passes even when `save` skips the write: it only checks the success flag. I reproduced this with an in-memory mutation, leaving `service.py` untouched. I’ll add an assertion on the store contents and rerun the mutation.

The original test missed a lost write: removing `store.append(record)` in an isolated in-memory mutation still passed.

Updated `test_service.py` to assert the store contains both the existing entry and the saved record.

Verified:
- Original implementation passes.
- Lost-write mutation fails the new assertion.
- `git diff --check` passes.

Production code is unchanged; no deliberate fault remains.
