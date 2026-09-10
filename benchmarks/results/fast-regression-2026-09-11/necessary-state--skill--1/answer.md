I’ll use the hostage-negotiator skill to keep this focused on pending save state and verify that Submit re-enables after both success and failure.

Implemented in `form.py`: `Form.pending` disables Submit during save and resets after success or failure. Duplicate submissions are ignored; return values and exceptions are preserved.

Verified pending state, duplicate prevention, success, failure, and retry. `git diff --check` passed.
