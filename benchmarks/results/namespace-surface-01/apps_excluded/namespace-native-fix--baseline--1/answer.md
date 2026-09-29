I’ll read the project instructions and code, run the tests before the fix, then change only `app.py` and rerun the same command.


Changed only `app.py`: `quantity()` now returns `2`. Payload behavior, tests, and existing owner changes in `notes.txt` were preserved.

`python3 -B -m unittest -v test_app`:
- Before: 2 tests, 1 failure (`1 != 2`), exit `1`.
- After: 2 tests passed, exit `0`.

Actual outputs and process exits are retained in the tool results.
