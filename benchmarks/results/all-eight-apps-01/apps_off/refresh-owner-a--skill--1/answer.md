I’ll use the hostage-negotiator skill to check the refresh contract, preserve existing notes, and add bounded async tests around the actual `Preview`.



`refresh` already guards value publication, but every call clears `pending` in `finally`. That lets an earlier call clear the latest call’s loading state. I’ll add regression tests before applying the matching ownership guard to cleanup.



The baseline run found five failures, all caused by an older call clearing `pending` while the latest refresh or retry remained unresolved. The other three tests passed. I’ll now guard cleanup with the existing generation check.



Fixed `Preview.refresh` so only the latest-started call clears `pending`. Overlapping calls remain independent.

Added eight standard-library tests covering all requested scenarios, with bounded waits, owned-task cleanup, and no timing sleeps. Requirements and owner notes remain unchanged.

Native `python3 -B -m unittest discover -v` results:

- Before fix: 8 tests, 5 failures; exit **1**.
- After fix: 8 tests, all **OK**; exit **0**.

Helper integrity and diff checks passed.
