I’ll read the requested skill and requirements, review `Preview.refresh`, and add controlled-callback tests. I’ll run the specified unittest command and report its output and exit code.

I’m using the hostage-negotiator skill to keep the change focused. `refresh` already limits value updates to the latest call, but every call clears `pending` in `finally`. An earlier call can therefore clear it while the latest is still waiting. I’ll test that ownership bug before fixing it.

The initial run reported four failures across five test methods, all showing an earlier call clearing `pending` while a newer call was unresolved; the process exited with code 1. I’ll guard the `finally` assignment with the existing generation check and rerun the suite.

Fixed `Preview.refresh` so only the latest-started call clears `pending`. Overlapping calls remain independent.

Added standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Actual `python3 -B -m unittest discover -v` results:
- Before fix: 5 tests, 4 failures; exit 1.
- After fix: 5 tests, all `OK`; exit 0.

`git diff --check` also passed.
