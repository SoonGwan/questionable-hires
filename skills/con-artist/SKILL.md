---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Start with the user-selected tests or changed behavior. Use the repository's documented test command, or the runner already evidenced by its test imports/configuration; don't guess a different framework or install one. Run that baseline and trace important assertions through implementation and mocks to identify the protected contract.

Choose a fault at the boundary the assertion could miss: acknowledged versus persisted, closed flag versus resource cleanup, latest request versus latest completion, full consumption versus early exit. A syntax error is not behavioral sensitivity. Establish a reachable input where the fault violates the contract; equivalent mutations prove nothing.

Match the experiment to the task size. For a small local audit, one disposable copy and a short inline command are enough; don't build an audit framework, standalone runner, or JSON report merely to record a few checks. Retain a reusable harness when the user needs one or the workflow actually repeats. Verify imports resolve to the copied implementation, and reuse a valid baseline rather than rerunning it unchanged.

Keep test configuration unchanged and vary one behavior at a time. Capture the test exit status separately from log-display commands. A killed mutant protects that fault, not every lifecycle path. Investigate another fault only when a distinct untested boundary matters to the requested contract; stop fishing for survivors.

If isolation or execution isn't available, report a static concern and proposed experiment, not a demonstrated survivor. Keep a failing baseline separate from mutation results.

## Deliver and stop

For a survivor, assert the externally meaningful effect, not just a returned success flag or final container size that could hide repeated writes. Confirm the same proposed regression passes correct code and fails the fault. For a killed mutant, explain the detecting assertion or warning policy. The decisive commands/results and proposed assertion in the answer can be the complete receipt; separate files are optional. Apply test improvements only when requested, never the deliberate fault.

Stop after the scoped coverage claims have been assessed and any requested improvement verified. Don't chase a global mutation score or demand every mock be removed.

## Working agreement

Preserve user changes and explicit requirements. Review is not permission to implement or publish. Locate relevant files from supplied paths or the actual repository file list before guessing framework-specific paths. Reuse existing artifacts; report decisive evidence without duplicating logs. Separate observation from inference; keep humor optional.
