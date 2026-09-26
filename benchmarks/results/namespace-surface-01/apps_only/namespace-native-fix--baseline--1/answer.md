I’ll read the project instructions and both files, run the tests before the fix, then update only `app.py` and rerun the tests, retaining the output and exit codes.

Changed `app.py` so `quantity()` returns `2`. Preserved payload behavior, tests, and the existing owner changes in `notes.txt`.

Ran `python3 -B -m unittest -v test_app`:
- Before: 2 tests, 1 failure (`1 != 2`); exit `1`.
- After: 2 tests passed; exit `0`.

Actual output and process exits are retained above.
