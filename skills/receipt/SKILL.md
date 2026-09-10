---
name: receipt
description: Verify that a requested bug fix changes observable behavior with a failing-before, passing-after reproduction and honest execution evidence.
---

# Receipt

> You fixed it? Show me the receipt.

## Collect a real receipt

Translate the reported bug into an observable failure and expected behavior. Reuse a focused existing test or build the smallest reproduction that exercises the real affected path. A compiler error or missing dependency is not a reproduction of an application bug.

Run the reproduction against the unfixed behavior when available. Record the command, relevant input, failure, and revision or diff context. If the fix already exists, use an isolated copy or worktree for a justified comparison; don't reverse patches in the user's dirty tree. If the old behavior cannot be run, say the before result is unavailable.

When asked to fix, implement the change and run the same meaningful check again. Confirm that inputs and assertions weren't weakened to obtain a pass. Run the surrounding checks appropriate to the changed contract. When asked only to verify, report findings without silently modifying production code.

A mocked response proves only the boundary the mock actually exercises. Match the claimed result to the tested layer. Distinguish a successful command from proof of the user's intended outcome.

## Deliver and stop

Give the behavior changed, before/after results, exact reproducible command, and remaining verification limits. Include a focused regression test when it meaningfully prevents recurrence. Never invent terminal output or call an unexecuted check passed.

Stop after the reproduction and relevant required checks establish the outcome. Don't collect unrelated green checks to make the receipt longer. A blocked environment is an unverified result, not a product failure or success.

## Working agreement

Follow the user's requested outcome and repository conventions. User instructions take precedence over this skill's preferences. Resolve routine choices from available context and keep working within authorized scope. Investigation is not permission to implement or publish. Preserve existing user changes.

Use the user's language. Keep the character to an optional short line; never insult people or substitute a joke for evidence. Report observed facts separately from inferences and unavailable checks. If a skill instruction actually prevents progress, cite that instruction and explain the concrete conflict.

