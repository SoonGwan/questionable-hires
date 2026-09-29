I’ll read the project instructions and both files, run the tests before and after the fix, and change only `app.py`.


Changed only `app.py`: `quantity()` now returns `2`. Preserved payload behavior, tests, and existing owner changes in `notes.txt`.

Ran `python3 -B -m unittest -v test_app`:
- Before: 2 tests, 1 failure; exit `1`.
- After: 2 tests passed; exit `0`.

Actual outputs and process exits are retained in the tool results.
