I’ll read the hostage-negotiator skill and requirements, review `Preview.refresh`, and add controlled concurrency tests. I’ll change `preview.py` only if needed, then run the requested unittest command and report its output and exit code.

`Preview.refresh` clears `pending` whenever any call settles. That lets an earlier call clear it while the latest is still waiting, contrary to the requirements. I’ll add regression tests first, then guard that cleanup with the existing generation check.

The baseline run found five failing subcases, all caused by an older call clearing `pending` while newer work remained unresolved. The test process exited with code 1. I’ll now apply the generation guard and rerun the suite.

Fixed `Preview.refresh` so only the latest-started call clears `pending`. Overlapping calls remain independent.

Added standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes were preserved.

Actual `python3 -B -m unittest discover -v` results:

- Before fix: 5 tests, 5 failing subcases; exit **1**.
- After fix: 5 tests, **OK**; exit **0**.

Diff checks and copied-helper integrity check passed.
