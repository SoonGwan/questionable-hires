I’m using the hostage-negotiator skill to keep this focused on Submit’s pending behavior. I’ll inspect the save flow, add the necessary state, and verify that Submit re-enables after both success and failure.

Implemented in [form.py](project/form.py).

- Added `pending` for Submit’s disabled state.
- Prevented duplicate saves while pending.
- Clears pending on success or failure, preserving return values and propagating errors.

Verified success, failure, duplicate prevention, and retry behavior. `git diff --check` passed.
