---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

## Visit like a real user

Trace the changed UI/request path to its visible success condition. Keep discovery, including instruction-file searches, inside an explicitly restricted project root.

Choose the shortest discriminating sequence: start an operation, cross a relevant state boundary, then complete or fail the earlier operation. Pair it with the nearest normal sequence. Reuse existing browser/test facilities or a small parameterized reproduction, not a new framework or hazard checklist. Control promises, responses or clocks rather than sleeps or permutations.

Observe actual submitted operations, latest selection, or recovered input/error/focus as appropriate. A disabled button doesn't prove server idempotency; mocked state doesn't prove rendered focus. Report a working guard honestly.

Bound behavior-dependent waits and clean up owned operations. Cancellation isn't termination: if it can be ignored, the runner's process deadline must also cover cleanup. Timeout means an incomplete check, not a reproduced defect.

Use local/designated test data, not real purchases, messages or destructive production actions. Without browser tooling, test the closest relevant state boundary and name untested browser behavior.

## Deliver and stop

Return the sequence, expected/observed outcome, tested layer and reproducible command—including any deadline needed for termination. A test-file link alone doesn't preserve its external runner. Reuse evidence instead of duplicating logs.

Preserve user changes; QA authorizes neither a production fix nor publication. Implement only when requested. Stop when relevant sequences and required checks cover the interaction. An unexecuted concern is not an observed defect.
