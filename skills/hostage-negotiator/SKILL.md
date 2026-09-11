---
name: hostage-negotiator
description: Keep a small requested change focused when optional refactors, architectural redesign, or unrelated cleanup threaten to expand its scope.
---

# Hostage Negotiator

> Release the button. The architecture stays.

## Establish the terms

Locate applicable instructions, requirements, affected code and existing tests within the allowed project root. Batch independent reads; consume their results before choosing dependent commands, including the documented test invocation. Follow unresolved dependencies, not guessed frameworks or repeated discovery.

For each supporting change, ask: which acceptance condition fails without it? A small visible change can require state, errors or security work; minimal diff size is not the objective. Separate optional refactors without creating a scope document for an ordinary edit. Ask only for a missing material product decision; adapt when the user changes the request.

For stateful behavior, follow entry, completion and recovery through the existing owner. Preserve return values, errors and cleanup, including cancellation. Reuse covered tests and add missing transitions at that boundary, not a parallel harness.

Async regression checks must terminate even when the guarded behavior is broken: bound behavior-dependent waits and release or cancel controlled tasks in cleanup.

## Deliver and stop

Review the diff against acceptance conditions, removing only your own unjustified additions. Reuse established verification. Deliver the change, decisive evidence and consequential limitations; distinguish observation from inference. Stop when requested behavior and required checks are satisfied, without opportunistic cleanup.

Preserve user changes and explicit requirements. Review does not authorize implementation; publishing and optional refactors require authorization. Keep humor optional.
