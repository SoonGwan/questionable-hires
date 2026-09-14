---
name: hostage-negotiator
description: Keep a small requested change focused when optional refactors, architectural redesign, or unrelated cleanup threaten to expand its scope.
---

# Hostage Negotiator

> Release the button. The architecture stays.

## Establish the terms

Reuse supplied paths and instructions. When locations are missing, discover applicable project instructions, affected code, contracts and tests together within the allowed root. Then batch the known relevant reads and working-tree status; do not repeat inventory or keyword searches for files already located. Search again for a specific unresolved dependency or instruction boundary. Choose the runner from the project, not a guessed framework.

For each supporting change, ask which acceptance condition fails without it. A small visible change can require state, error handling or security work; smallest diff is not the objective. Keep optional refactors separate, without creating a scope document for an ordinary edit. Ask when a missing product decision materially changes the implementation.

For stateful behavior, follow entry, completion and recovery through the existing owner. Preserve return values, errors and cleanup, including cancellation. Reuse covered tests and add missing transitions at that boundary, not a parallel harness.

When asserting that stale or failed work leaves state unchanged, capture the relevant field values before releasing that work and compare them afterward. Retaining the state object itself can alias in-place mutations. Preserve payload/error references when identity is contractual; snapshot nested mutable contents only where the contract requires their stability.

Async regression checks must terminate even when the guarded behavior is broken: bound behavior-dependent waits and release or cancel controlled tasks in cleanup.

For Python asyncio callback tests without equivalent project support, read and copy the optional [controlled-call asset](assets/controlled_call.py); its module docstring contains the usage and limits. It replaces repeated entry/release gates, not application assertions. No separate reference is needed for this path.

For JavaScript Promise callbacks without equivalent support, use the optional [ES-module asset](assets/controlled_call.mjs) instead. Read its opening usage comment first (`sed -n '1,/^ \*\//p' <asset-path>`), alongside the known application files, and copy the module into permitted test support. To check an unchanged copy, use `cmp <asset-path> <copy-path>` and its exit status rather than printing the module again. Inspect implementation when adapting it or resolving unclear behavior. The comment covers both plain calls and optional `withControlledCalls` lifecycle ownership. Read only the resource for the actual runtime; tests still own application assertions and external-resource cleanup.

## Deliver and stop

Review the diff against acceptance conditions, removing only your own unjustified additions. Reuse established verification; repeat when requested or when changed state, nondeterminism or a remaining uncertainty warrants it. When batching tests with diff/status, preserve the test's exit rather than the last command's success. Confirm required checks actually ran from their result output; missing output or undiscovered/skipped tests cannot support a pass claim. Inspect existing evidence first and rerun only the unresolved, safely repeatable check when needed. Report decisive observations and consequential limitations, separating inference. Stop when requested behavior and required checks are satisfied, without opportunistic cleanup.

Preserve user changes and explicit requirements. Review does not authorize implementation; publishing and optional refactors require authorization. Keep humor optional.
