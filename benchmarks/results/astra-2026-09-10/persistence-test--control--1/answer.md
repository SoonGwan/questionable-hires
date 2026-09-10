I’ll inspect the test and write path, then run an isolated mutation to see whether the test detects a lost write.

The test misses the lost write: it passes when an in-memory mutation removes `store.append(record)` but still returns success. I’ll add an assertion on the store’s contents and verify that the same mutation fails.

The original test missed a lost write because it checked only `ok`.

Updated `test_service.py` to assert that the store contains the record. Verified with an isolated, in-memory mutation removing `store.append(record)`:

- Original test: passed despite the lost write.
- Updated test: failed on the missing record.
- Production implementation: passed the updated test.

`service.py` is unchanged; `git diff --check` passed.
