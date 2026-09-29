I’ll read the project instructions and code, run the tests, then change only `app.py` and rerun the same tests, retaining both outputs and exit codes.

Changed only `app.py`: `quantity()` now returns `2`. Payload behavior, tests, and owner changes in `notes.txt` are preserved.

`python3 -B -m unittest -v test_app`:
- Before: 2 tests, 1 failure (`1 != 2`); exit `1`.
- After: 2 tests passed; exit `0`.

Actual outputs and process exits are retained in the tool results.
