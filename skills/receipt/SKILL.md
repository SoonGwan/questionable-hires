---
name: receipt
description: Verify that a requested bug fix changes observable behavior with a failing-before, passing-after reproduction and honest execution evidence.
---

# Receipt

> You fixed it? Show me the receipt.

## Prove the behavior, not the ceremony

Use one stable assertion on the real affected path, preferably in the existing regression test. Prefer the project's documented test command, including its runtime executable, over a guessed runner. Reuse an available before result when its input, implementation and failure reason are established; don't restart verification merely because this skill was loaded.

When implementing a fix, observe that assertion fail for the reported reason, change the implementation, then rerun the unchanged assertion. Missing dependencies or compiler errors are not reproduction of the reported defect. Add a neighboring input only when it distinguishes the intended fix from an overbroad one; run other checks required by the project or affected contracts.

If the fix already exists, compare in an isolated copy when needed; never reverse patches in the user's dirty tree. If the old behavior cannot run, mark before evidence unavailable. Verification alone does not authorize production edits or publication.

Keep each check's exit status identifiable: later printing or Git commands must not mask failure. A mock proves only its exercised boundary, not an unobserved downstream effect.

Deliver the behavior changed, before/after evidence with command and revision or diff context, and verification limits. Reuse the test and concise results as the receipt; no separate evidence dossier or unrelated green checks. Stop once the requested outcome and required checks are established. Preserve user changes; never present inferred or unexecuted results as observed.
