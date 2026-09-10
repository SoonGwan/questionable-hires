---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Start with the user-selected tests or changed behavior. Run the baseline and trace each important assertion through the actual implementation and mocks. Identify the contract supposedly protected.

Choose a fault at the boundary the assertion could miss: acknowledged versus persisted, closed flag versus resource cleanup, latest request versus latest completion, full consumption versus early exit. A syntax error is not behavioral sensitivity. Establish a reachable input where the fault violates the contract; equivalent mutations prove nothing.

Use one reusable isolated workspace, verify its imports resolve to the mutated implementation, and keep the baseline/test configuration unchanged. Change one behavior at a time; record the command and exit status separately from log-display commands. A killed mutant protects that fault, not every lifecycle path. Investigate another fault only when a distinct untested boundary matters to the requested contract; stop fishing for survivors.

If isolation or execution isn't available, report a static concern and proposed experiment, not a demonstrated survivor. Keep a failing baseline separate from mutation results.

## Deliver and stop

For a survivor, assert the externally meaningful effect, not just a returned success flag or final container size that could hide repeated writes. Confirm the same proposed regression passes correct code and fails the fault. For a killed mutant, explain the detecting assertion or warning policy. Leave a compact evidence artifact; apply test improvements only when requested, never the deliberate fault.

Stop after the scoped coverage claims have been assessed and any requested improvement verified. Don't chase a global mutation score or demand every mock be removed.

## Working agreement

Preserve user changes and explicit requirements. Review is not permission to implement or publish. Separate observed evidence from inference; keep humor optional. Reuse existing artifacts and report decisive evidence without duplicating full logs.
