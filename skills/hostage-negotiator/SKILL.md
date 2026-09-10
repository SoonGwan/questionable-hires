---
name: hostage-negotiator
description: Keep a small requested change focused when optional refactors, architectural redesign, or unrelated cleanup threaten to expand its scope.
---

# Hostage Negotiator

> Release the button. The architecture stays.

## Establish the terms

Recover the user's concrete requested behavior and acceptance conditions from the conversation. Inspect the affected code and existing conventions. Identify which changes are required to deliver that behavior and which would only improve adjacent code.

For each proposed supporting change, ask whether omitting it makes an acceptance condition fail. If yes, trace that dependency into scope; otherwise defer it. Implement along the existing path when viable. Simple label changes need no architecture survey; pending/retry behavior may require state changes even when the visible request looks small.

Keep optional improvements out of the implementation unless authorized. Mention a consequential deferred issue briefly if useful, without turning it into a new task or approval ceremony. Never hide a real correctness or security requirement to meet an arbitrary diff budget.

Use routine project choices without asking the user to redesign the task. If a material product decision is genuinely missing, prepare independent work and ask only for that decision. When the user expands the scope, update the terms rather than enforcing an obsolete restriction.

## Deliver and stop

Before delivery, map changed production hunks to acceptance conditions or necessary dependencies. Remove only your own unjustified additions, never user work. Verify the affected behavior at its existing test boundary; don't create a test framework for a static edit. For a scope review, explain optional hunks without rewriting them.

Stop when the agreed behavior and required checks are satisfied. Don't add cleanup merely because you have time left.

## Working agreement

Preserve user changes and explicit requirements. Review is not permission to implement or publish. Locate relevant files from supplied paths or the actual repository file list before guessing framework-specific paths. Reuse existing artifacts; report decisive evidence without duplicating logs. Separate observation from inference; keep humor optional.
