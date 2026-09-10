---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

## Visit like a real user

Trace the changed journey's UI and request handling to its externally visible success condition. Choose a sequence that can violate it, not a generic checklist of interaction hazards.

Use the shortest discriminating sequence: start an operation, cross a relevant state boundary, then complete or fail the earlier operation. Pair it with the nearest normal sequence. Control promises, responses or clocks in one reusable harness rather than adding sleeps or enumerating permutations. Use existing browser facilities when available.

Observe the actual effect: submitted operations for duplicate prevention, latest selection after late responses, input/error/focus after recovery. A disabled button doesn't prove server idempotency; mocked state doesn't prove rendered focus. When a guard holds, report that result rather than inventing a failure.

Use local or designated test data, not real purchases, messages or destructive production actions. Without browser tooling, exercise the closest relevant state boundary and name the untested browser behavior.

## Deliver and stop

Report the sequence, expected versus observed outcome, decisive evidence and tested layer. Reuse the reproduction instead of duplicating its logs. Add a fix only when requested, preserving user changes and scope; QA does not authorize implementation or publication. Stop once the relevant sequences and required checks cover the requested interaction. An unexecuted concern is not an observed defect.
