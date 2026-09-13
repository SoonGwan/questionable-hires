---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Trace the selected assertions through implementation and mocks to the contract they actually protect. Keep discovery, including instruction-file searches, inside an explicitly restricted project root. Use the documented test command or evidenced runner, not a new framework. Reuse a valid baseline; a failing baseline is not a mutation result.

Choose a reachable fault at an unobserved boundary: acknowledgment versus persistence, closed flag versus cleanup, latest request versus completion, full consumption versus early exit. Syntax errors and behaviorally equivalent mutations do not establish sensitivity to the intended fault.

Reuse an established project audit or valid evidence first. Choose isolation by the semantic context it must preserve, not the apparent size of the experiment. A fresh-process in-memory substitution fits when the actual caller resolves it and the original compilation context and bindings remain intact. Extracting function text alone can lose module future flags, closures or decorators; use a disposable module/package copy when reconstructing that context would add work or uncertainty. Don't replace the implementation with a fake or mistake a wrong binding for a surviving fault. Restore substitutions within a reused process and keep original files intact.

For a Python audit that needs disposable copies and correct/faulty test runs, use
[the audit helper](references/python-audit.md) when its file, interpreter and runner
limits fit. It collects labeled phase results in one invocation; don't write a
copy/subprocess/cleanup wrapper just to orchestrate those same phases. Existing
adequate project audits and simpler valid in-memory substitutions still take
precedence. Unsupported layouts need project facilities, not forced adaptation.
Preserve test configuration, vary one behavior, and capture each phase's own exit
status. Check copied-import paths and caller bindings in the actual test/probe
process where practical; a separate import-only process does not prove what tests
load. Retain a harness only for requested reuse or delivery; source inspection is
appropriate for trust review, adaptation or troubleshooting.

If the original test survives, check the meaningful effect—not merely success or container size that could hide repeated writes. Run the same stronger assertion against correct and faulty implementations: it must pass the former and fail the latter for the intended reason. If the mutant is killed, identify the detecting assertion or warning policy; this protects that fault, not all lifecycle paths.

## Deliver and stop

Give decisive commands/results, the coverage gap or detecting check, and the proposed assertion. No separate report files are required. Without isolation or execution, label the concern static, not a demonstrated survivor. Apply test improvements only when requested, never the deliberate fault; an audit does not authorize publication.

Stop when the scoped claim is assessed and requested improvements are verified. Try another fault only for a distinct boundary material to that claim; don't fish for survivors, chase a global mutation score, or remove every mock.
