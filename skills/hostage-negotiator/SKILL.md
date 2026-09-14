---
name: hostage-negotiator
description: Keep a small requested change focused when optional refactors, architectural redesign, or unrelated cleanup threaten to expand its scope.
---

# Hostage Negotiator

> Release the button. The architecture stays.

## Establish the terms

Reuse supplied paths and instructions. When locations are missing, discover applicable project instructions, affected code, contracts and tests together within the allowed root. Then batch the known relevant reads and working-tree status; do not repeat inventory or keyword searches for files already located. Search again for a specific unresolved dependency or instruction boundary. Choose the runner from the project, not a guessed framework.

For each supporting change, ask which acceptance condition fails without it. A small visible change can require state, error handling or security work; smallest diff is not the objective. Keep optional refactors separate, without creating a scope document for an ordinary edit. Ask when a missing product decision materially changes the implementation.

For stateful behavior, follow entry, completion and recovery through the existing owner. Preserve existing or specified return values, errors and cleanup, including cancellation. For a newly suppressed operation, assert the required suppression and state ownership without inventing an unspecified return-value contract. Reuse covered tests and add missing transitions at that boundary, not a parallel harness.

When asserting that stale or failed work leaves state unchanged, capture the relevant field values before releasing that work and compare them afterward. Retaining the state object itself can alias in-place mutations. Preserve payload/error references when identity is contractual; snapshot nested mutable contents only where the contract requires their stability.

Async regression checks must terminate even when the guarded behavior is broken: bound behavior-dependent waits and release or cancel controlled tasks in cleanup.

For Python asyncio callback tests without equivalent project support, read and copy the optional [controlled-call asset](assets/controlled_call.py); its module docstring contains the usage and limits. It replaces repeated entry/release gates, not application assertions. No separate reference is needed for this path.

For JavaScript Promise callbacks without equivalent support, use the optional [ES-module asset](assets/controlled_call.mjs) instead. Read its opening usage comment first (`sed -n '1,/^ \*\//p' <asset-path>`), alongside the known application files, and copy the module into permitted test support. To check an unchanged copy, use `cmp <asset-path> <copy-path>` and its exit status rather than printing the module again. Inspect implementation when adapting it or resolving unclear behavior. The comment covers both plain calls and optional `withControlledCalls` lifecycle ownership. Read only the resource for the actual runtime; tests still own application assertions and external-resource cleanup.

## Deliver and stop

After edits, batch remaining native tests, copy-integrity checks and final diff/status in one shell call when no intervening decision is needed. Use `&&` to stop on failure; later checks are then unrun. If every check must run regardless, retain each exit separately: a final successful status command must not hide a failed test or copy check. Do not recopy an existing helper merely to make its integrity check pass.

Review the diff against acceptance conditions, removing only your own unjustified additions. Reuse valid execution evidence; rerun only for changed relevant inputs, unresolved uncertainty or an explicit requirement. Missing output or undiscovered/skipped tests cannot support a pass. Report decisive observations and limits, then stop when the requested behavior and checks are verified.

Preserve user changes and explicit requirements. Review does not authorize implementation; publishing and optional refactors require authorization. Keep humor optional.
