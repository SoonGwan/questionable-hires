I’ll read `requirements.md` and the existing Publisher, add the duplicate guard and regressions, then run both the existing and new tests.

The Publisher now tracks pending document IDs per instance and clears each entry in `finally`, covering success, failure, and cancellation. The regressions check that duplicates return while the first write stays blocked, and that different keys and instances can enter their callbacks concurrently. The original two tests passed before the change.

Implemented per-instance duplicate suppression with cleanup after success, failure, or cancellation. Added seven bounded regressions with task cleanup. Existing tests and unrelated files remain unchanged.

Observed results:
- Full suite: 9 tests passed.
- Regression rerun: 7 tests passed.
- `git diff --check`: passed.
