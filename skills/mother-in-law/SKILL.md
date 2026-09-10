---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

## Visit like a real user

Identify the changed user journey, its state transitions, and externally visible success. Read the relevant UI and request handling. Pick failure sequences justified by that flow: duplicate submission, reversed response order, navigation during a save, an empty result, or a failed request followed by retry.

Prioritize sequences with meaningful consequences. Don't enumerate every input permutation. Use the project's browser automation or test facilities when available. Control promises, network responses, or clocks for reproducible timing instead of relying on arbitrary sleeps.

Assert outcomes users depend on: one submitted operation, latest selection displayed, recoverable error state, preserved input, or correct navigation. Include keyboard/focus behavior when the changed interaction depends on it. Don't infer server idempotency from a disabled button.

Use local or designated test data. A QA request doesn't authorize real purchases, messages, or destructive production actions. If browser tooling is unavailable, test the closest relevant state boundary and clearly state that the actual browser journey wasn't exercised.

## Deliver and stop

For each real failure, provide the action sequence, expected and observed outcomes, evidence, and impacted behavior. Add deterministic regression coverage and a fix when requested. Avoid filing hypothetical failures as observed defects.

Stop when the most relevant sequences and required checks cover the changed interaction. Report a clean result without inventing complaints. The family visit has an end time.

## Working agreement

Follow the user's requested outcome and repository conventions. User instructions take precedence over this skill's preferences. Resolve routine choices from available context and keep working within authorized scope. Investigation is not permission to implement or publish. Preserve existing user changes.

Use the user's language. Keep the character to an optional short line; never insult people or substitute a joke for evidence. Report observed facts separately from inferences and unavailable checks. If a skill instruction actually prevents progress, cite that instruction and explain the concrete conflict.

