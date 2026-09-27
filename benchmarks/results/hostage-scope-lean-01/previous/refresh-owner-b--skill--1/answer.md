I’ll read the requested skill and refresh requirements, review `Preview.refresh`, and add controlled-callback tests. I’ll change `preview.py` only if needed, then run the requested unittest command.


`Preview.refresh` appears to meet the requirements: every call invokes its callback, and the generation check limits publication and pending-state cleanup to the latest call. I’ll leave it unchanged and test overlapping success, failure, cancellation, retry, and instance isolation.


`Preview.refresh` meets the requirements; no implementation change was needed.

Added 9 standard-library tests in `test_preview.py` covering the requested scenarios, with bounded waits, task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Native run: `python3 -B -m unittest discover -v`
Result: **9 tests ran, all OK. Process exit: 0.**
