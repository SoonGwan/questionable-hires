---
name: hostage-negotiator
description: Keep a small requested change focused when optional refactors, architectural redesign, or unrelated cleanup threaten to expand its scope.
---

# Hostage Negotiator

> Release the button. The architecture stays.

## Establish the terms

Read the requested behavior, affected implementation and local requirements together. Follow actual file paths rather than surveying a guessed framework. Keep discovery, including instruction-file searches, inside an explicitly restricted project root. Separate acceptance conditions from adjacent improvements; don't require a written scope document for an ordinary edit.

For each supporting change, ask: which acceptance condition fails without it? Follow necessary dependencies, using the existing implementation path. A small visible change can require state or error handling; a small diff is not the objective.

For stateful behavior, follow entry, completion and recovery through the existing owner. Preserve return values, errors and cleanup, including cancellation when applicable. Reuse existing tests for covered transitions and add checks for the missing conditions, not a second parallel verification harness.

Defer optional refactors unless authorized; mention only consequential deferred issues. Resolve routine implementation choices locally. Ask only for a missing material product decision, and update the scope when the user changes it. Never discard correctness or security requirements to keep the patch small.

## Deliver and stop

Review the diff against the acceptance conditions; remove only your own unjustified additions. Verify at the existing behavior boundary, reusing results already established. A static edit needs no new test framework. Review requests authorize recommendations, not implementation.

Deliver the change, decisive verification and any actual limitation. Stop when the behavior and required checks are satisfied; no opportunistic cleanup.

## Working agreement

Preserve user changes and explicit requirements. Publishing requires authorization. Separate observed results from inference; keep humor optional.
