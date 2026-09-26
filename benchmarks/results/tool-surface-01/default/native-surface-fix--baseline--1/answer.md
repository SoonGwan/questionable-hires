I’ll read the project instructions and code, run the required tests before the fix, then update only `app.py` and rerun them.


The baseline run exited with code 1: `quantity()` returned 1 where the test requires 2; the payload test passed. I’ll change that return value. The existing owner change in `notes.txt` will remain untouched.


Changed only `app.py`: `quantity()` now returns `2`. Preserved payload behavior, tests, and owner changes in `notes.txt`.

`python3 -B -m unittest -v test_app`:
- Before: 2 tests, 1 failure; exit code `1`.
- After: 2 tests passed; exit code `0`.

Actual output and process exits are retained in the tool results.
