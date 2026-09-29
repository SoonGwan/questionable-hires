I’ll read the project instructions and code, run the tests before and after the fix, and change only `app.py`.


The baseline run exited with code 1: `quantity()` returned 1, but the test requires 2. The payload test passed. I’ll update that return value.


Changed only `app.py`: `quantity()` now returns `2`. Preserved payload behavior, tests, and the owner’s `notes.txt` changes.

`python3 -B -m unittest -v test_app`:
- Before: 2 tests, 1 failure; exit code 1.
- After: 2 tests passed; exit code 0.

Actual outputs and process exits are retained in the tool results.
