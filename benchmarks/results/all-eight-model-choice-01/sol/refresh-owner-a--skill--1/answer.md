I’m applying the hostage-negotiator skill to keep the review focused. I’ll read the requirements, `Preview.refresh`, project instructions, and working-tree status, then add controlled async regression tests and change `preview.py` only if the behavior requires it.

The current `finally` block lets an earlier call clear `pending` while the latest call is still unresolved. I’ll make that cleanup conditional on ownership and add tests that exercise overlapping calls through the real `Preview` instance.

The native unittest run passed all five discovered tests, including both completion orders and the failure and cancellation paths. I’ll check the final diff and copied helper integrity before reporting the scope and result.

`Preview.refresh` needed one fix: an earlier call could clear `pending` while the latest call was still unresolved. It now clears `pending` only when that call still owns the state.

I added [unittest coverage](project/test_preview.py) using controlled callbacks for both completion orders, failure and cancellation, retry, synchronous callback failure, identity, display retention, and instance isolation. Overlapping refreshes remain allowed. `requirements.md` and the unrelated owner note were preserved.

`python3 -B -m unittest discover -v` ran **5 tests: OK; process exit 0**.
