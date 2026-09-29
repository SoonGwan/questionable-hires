I’ll read the requested skill and requirements, review `Preview.refresh`, then add controlled concurrency tests and run the specified unittest command.

`Preview.refresh` appears to meet the requirements: each call invokes its callback, and only the latest-started call can publish or clear `pending`. I’m using the hostage-negotiator skill to keep this focused. I’ll leave `preview.py` unchanged unless the tests expose a defect, and use controlled callbacks with bounded task cleanup.

All eight tests passed in the native unittest run, with process exit `0`. No production change was needed. I’m checking the final scope and copied helper integrity before wrapping up.

`Preview.refresh` meets the requirements; `preview.py` needed no changes.

Added eight standard-library tests covering all requested scenarios, using actual `Preview`, controlled callbacks, bounded waits, and owned-task cleanup. Requirements and owner notes remain unchanged.

Actual run: `python3 -B -m unittest discover -v`
Result: **8 tests passed (`OK`), process exit 0**.
