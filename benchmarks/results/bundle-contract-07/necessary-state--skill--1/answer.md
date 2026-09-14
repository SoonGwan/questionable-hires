I’ll use the hostage-negotiator skill to keep the change focused, add the required regression coverage, and preserve unrelated work.

The UI already uses `Form.pending` to disable Submit. I’ll add per-instance state and clear it in `finally` so success, failure, and cancellation all restore the button. There’s no existing test runner; I’ll use standard-library `unittest` with the skill’s controlled callback helper.

Implemented per-instance `pending` state to disable Submit during save, prevent overlapping duplicates, and re-enable after success, failure, or cancellation.

All 5 regression tests pass, covering every requested behavior, bounded waits, and owned-task cleanup. Unrelated files were preserved.

Rerun with:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```
