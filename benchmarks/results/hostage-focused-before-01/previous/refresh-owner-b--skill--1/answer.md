I’ll use the requested hostage-negotiator skill, review `Preview.refresh` against the requirements, and add controlled-callback tests before running the specified unittest command.

`Preview.refresh` already appears to meet the requirements: its generation check gives the latest call ownership of display and pending state, and `finally` handles failure and cancellation. I’ll leave it unchanged and test the overlapping-call transitions with bounded waits and task cleanup.

All eight tests passed in the native unittest run, and the test process exited with code 0. They cover the requested completion orders, failures, cancellations, retry, identity, display retention, and instance isolation. I’m checking that the final changes preserve the implementation, requirements, and owner note.

`Preview.refresh` meets the requirements; `preview.py` needed no changes.

Added eight standard-library tests covering all requested scenarios, using actual `Preview`, controlled callbacks, bounded waits, and owned-task cleanup. Requirements and owner notes remain unchanged.

Native command: `python3 -B -m unittest discover -v`

Result: **Ran 8 tests in 0.039s — OK. Process exit: 0.**
