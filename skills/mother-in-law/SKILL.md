---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

## Visit like a real user

Identify the changed user journey, its state transitions, and externally visible success. Read the relevant UI and request handling. Pick failure sequences justified by that flow: duplicate submission, reversed response order, navigation during a save, an empty result, or a failed request followed by retry.

Choose the shortest sequence that could violate the journey's invariant: start an operation, cross a meaningful state boundary, then complete or fail the earlier operation. Pair it with the nearest normal sequence to distinguish a race from a generally broken flow. Reuse one harness with controlled promises, responses, or clocks; avoid arbitrary sleeps and exhaustive permutations. Use the project's browser facilities when available.

Observe the effect at its owner: count submitted operations for duplicate prevention, assert latest selection after late responses, and check input/error/focus after recovery when relevant. A disabled button doesn't prove server idempotency; a mocked state transition doesn't prove rendered focus behavior. Prioritize consequential failures over additional screenshots of a passing path.

Use local or designated test data. A QA request doesn't authorize real purchases, messages, or destructive production actions. If browser tooling is unavailable, test the closest relevant state boundary and clearly state that the actual browser journey wasn't exercised.

## Deliver and stop

For each real failure, provide the action sequence, expected and observed outcomes, evidence, and impacted behavior. Add deterministic regression coverage and a fix when requested. Avoid filing hypothetical failures as observed defects.

Stop when the most relevant sequences and required checks cover the changed interaction. Report a clean result without inventing complaints. The family visit has an end time.

## Working agreement

Preserve user changes and explicit requirements. Review is not permission to implement or publish. Locate relevant files from supplied paths or the actual repository file list before guessing framework-specific paths. Reuse existing artifacts; report decisive evidence without duplicating logs. Separate observation from inference; keep humor optional.
