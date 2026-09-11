---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Trace the selected assertions through implementation and mocks to the contract they actually protect. Use the documented test command or evidenced runner, not a new framework. Reuse a valid baseline; a failing baseline is not a mutation result.

Choose a reachable fault at an unobserved boundary: acknowledgment versus persistence, closed flag versus cleanup, latest request versus completion, full consumption versus early exit. Syntax errors and behaviorally equivalent mutations do not establish sensitivity to the intended fault.

For a small audit, use one disposable copy and a short inline experiment; retain a harness only when needed for reuse or delivery. Verify imports resolve to that copy. Preserve the user's original files, test configuration and explicit scope; vary one behavior at a time. Keep test exit statuses identifiable independently of log printing.

For small Python unittest/pytest audits, [the optional audit helper](references/python-audit.md) handles copies, exact mutation, import checks and separate test/probe outcomes. Read that reference when using it instead of rewriting the isolation plumbing. Keep the existing workflow when a helper would add setup or repeat already collected evidence.

If the original test survives, check the meaningful effect—not merely success or container size that could hide repeated writes. Run the same stronger assertion against correct and faulty implementations: it must pass the former and fail the latter for the intended reason. If the mutant is killed, identify the detecting assertion or warning policy; this protects that fault, not all lifecycle paths.

## Deliver and stop

Give decisive commands/results, the coverage gap or detecting check, and the proposed assertion. No separate report files are required. Without isolation or execution, label the concern static, not a demonstrated survivor. Apply test improvements only when requested, never the deliberate fault; an audit does not authorize publication.

Stop when the scoped claim is assessed and requested improvements are verified. Try another fault only for a distinct boundary material to that claim; don't fish for survivors, chase a global mutation score, or remove every mock.
