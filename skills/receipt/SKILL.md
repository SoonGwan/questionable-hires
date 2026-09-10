---
name: receipt
description: Verify that a requested bug fix changes observable behavior with a failing-before, passing-after reproduction and honest execution evidence.
---

# Receipt

> You fixed it? Show me the receipt.

## Collect a real receipt

Turn the reported bug into one stable observable assertion on the real affected path. Prefer adding it to the existing regression test over writing separate throwaway before/after scripts. Include a neighboring input when it distinguishes the intended boundary from an overbroad fix. A compiler error or missing dependency is not the bug reproduction.

Run the reproduction against the unfixed behavior when available. Record the command, relevant input, failure, and revision or diff context. If the fix already exists, use an isolated copy or worktree for a justified comparison; don't reverse patches in the user's dirty tree. If the old behavior cannot be run, say the before result is unavailable.

For a fix, first observe the assertion fail for the reported reason, then change the implementation and rerun that unchanged assertion. Add surrounding checks only for contracts the diff can affect. Keep command exit status separate from later printing or Git commands so a successful final shell command cannot mask a failed check. Verification-only requests do not authorize production edits.

A mocked response proves only the boundary the mock actually exercises. Match the claimed result to the tested layer. Distinguish a successful command from proof of the user's intended outcome.

## Deliver and stop

Give the behavior changed, before/after results, exact reproducible command, and remaining verification limits. Include a focused regression test when it meaningfully prevents recurrence. Never invent terminal output or call an unexecuted check passed.

Stop after the reproduction and relevant required checks establish the outcome. Don't collect unrelated green checks to make the receipt longer. A blocked environment is an unverified result, not a product failure or success.

## Working agreement

Preserve user changes and explicit requirements. Review is not permission to implement or publish. Locate relevant files from supplied paths or the actual repository file list before guessing framework-specific paths. Reuse existing artifacts; report decisive evidence without duplicating logs. Separate observation from inference; keep humor optional.
