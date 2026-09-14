I’ll use the hostage-negotiator skill to review `Preview.refresh`, make any required fix, and add controlled async tests within this project.



`Preview.refresh` appears to meet the requirements: its generation checks give the latest call ownership, and `finally` handles failures and cancellation, including synchronous callback failure. I’ll leave `preview.py` unchanged and test those transitions with independently controlled callbacks.



`Preview.refresh` meets the requirements; no implementation change was needed.

Added 8 rerunnable tests using actual `Preview` and controlled callbacks, covering all requested scenarios with bounded waits, task cleanup, and no timing sleeps.

`python3 -B -m unittest discover -v` reported **8 tests, OK**. Test process exit: **0**.

Requirements and owner notes remain unchanged.
