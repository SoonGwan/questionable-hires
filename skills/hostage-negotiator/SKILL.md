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

Without equivalent project support, use the optional [Python asyncio asset](assets/controlled_call.py) or [JavaScript Promise asset](assets/controlled_call.mjs), only for the actual runtime. Read Python's module docstring or JavaScript's opening usage comment alongside known application files; copy into permitted test support. Usage and limits live there, including optional JS lifecycle ownership. Inspect implementation for trust, adaptation or unclear behavior. Use `cmp <asset-path> <copy-path>` to check an unchanged copy, not another full read. Assets replace repeated entry/release gates, not application assertions or external-resource cleanup; no separate reference is needed.

## Deliver and stop

After edits, batch remaining native tests, copy-integrity checks and final diff/status in one shell call when no intervening decision is needed. Use `&&` to stop on failure; later checks are then unrun. If every check must run regardless, retain each exit separately: a final successful status command must not hide a failed test or copy check. Do not recopy an existing helper merely to make its integrity check pass.

Review the diff against acceptance conditions, removing only your own unjustified additions. Reuse valid evidence; rerun only for changed relevant inputs, unresolved uncertainty or an explicit requirement.

Before claiming tests passed, locate their native identities/count and results, not just the shell exit or trailing diff/status. Missing evidence: first inspect an existing report tied to that command and inputs; observe a still-running process instead of restarting it. Otherwise rerun only the missing, safely repeatable check in scope, capturing its result and own exit. Never replay a deployment or side-effectful workflow merely to recover output. If evidence remains unavailable, say unverified. A later run is new evidence, not a repaired transcript; missing, undiscovered or skipped tests cannot support a pass.

Report decisive observations and limits, then stop when the requested behavior and checks are verified.

Preserve user changes and explicit requirements. Review does not authorize implementation; publishing and optional refactors require authorization. Keep humor optional.
