I’ll use the hostage-negotiator skill to review `Preview.refresh`, make any required fix, and add controlled async tests within this project.

`Preview.refresh` already matches the requirements: generation checks protect display updates and pending state, and `finally` handles failure and cancellation, including a synchronous callback exception. I’ll leave `preview.py` unchanged and add tests for overlapping calls, state retention, and recovery.

The tests now cover both success orders, failure and cancellation ownership, retry, synchronous failure, object identity, prior display retention, and instance isolation. Each test owns and cleans up its tasks, uses bounded waits, and releases callbacks explicitly without timing sleeps. I’ll run the requested unittest command and check the final diff.

`Preview.refresh` already satisfies `requirements.md`; no production fix was needed.

Added 8 rerunnable unittest tests covering all requested scenarios, using actual `Preview`, controlled callbacks, bounded waits, task cleanup, and no timing sleeps.

Native result from `python3 -B -m unittest discover -v`: **8 tests, all OK; test process exit 0**. Helper integrity and diff checks also passed.

Requirements and unrelated owner notes remain unchanged.
