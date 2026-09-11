---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Trace the selected assertions through implementation and mocks to the contract they actually protect. Keep discovery, including instruction-file searches, inside an explicitly restricted project root. Use the documented test command or evidenced runner, not a new framework. Reuse a valid baseline; a failing baseline is not a mutation result.

Choose a reachable fault at an unobserved boundary: acknowledgment versus persistence, closed flag versus cleanup, latest request versus completion, full consumption versus early exit. Syntax errors and behaviorally equivalent mutations do not establish sensitivity to the intended fault.

Choose the isolation path before writing a harness. Reuse an established project audit or valid evidence first. For a new small Python unittest/pytest audit, prefer [the supplied helper](references/python-audit.md) when its supported layout and limits fit: provide the fault and assertions, rather than rewriting copy/import/status plumbing. Read its interface and invoke the CLI; source inspection remains appropriate for trust review, adaptation or troubleshooting.

Use a small native inline experiment for unsupported runtimes/layouts or when the helper would add setup or repeat evidence. Preserve original files and test configuration, verify imports from the isolated copy, vary one behavior, and capture each test's own exit status. Retain a harness only for requested reuse or delivery; small size alone isn't a reason to reimplement existing isolation machinery.

If the original test survives, check the meaningful effect—not merely success or container size that could hide repeated writes. Run the same stronger assertion against correct and faulty implementations: it must pass the former and fail the latter for the intended reason. If the mutant is killed, identify the detecting assertion or warning policy; this protects that fault, not all lifecycle paths.

## Deliver and stop

Give decisive commands/results, the coverage gap or detecting check, and the proposed assertion. No separate report files are required. Without isolation or execution, label the concern static, not a demonstrated survivor. Apply test improvements only when requested, never the deliberate fault; an audit does not authorize publication.

Stop when the scoped claim is assessed and requested improvements are verified. Try another fault only for a distinct boundary material to that claim; don't fish for survivors, chase a global mutation score, or remove every mock.
