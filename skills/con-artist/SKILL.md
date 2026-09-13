---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Start from the requested assertions and follow their actual calls through implementation and mocks. Read the reached definitions and relevant fixtures/configuration; broaden discovery when a dependency or contract remains unresolved, not merely because more files exist. Reuse completed project-scoped instruction discovery and known runner information after loading this skill. Keep any new discovery inside the permitted project root.

Use the documented command or evidenced runner, preserving test configuration. Reuse a valid baseline or established audit; a failing baseline is not mutation evidence. Choose one reachable behavioral fault at the requested boundary, such as acknowledgment versus persistence or closed flag versus cleanup. Syntax errors and equivalent mutations do not establish sensitivity.

Choose isolation by the context it preserves. In-memory substitution fits when the actual caller resolves it and compilation context/bindings remain intact; restore substitutions in reused processes. Extracting function text can lose future flags, closures or decorators: use disposable module/package copies when that context is uncertain. Keep originals intact; a fake implementation or wrong binding does not demonstrate a surviving fault.

For compatible Python copy-based audits, use [the audit helper](references/python-audit.md)
instead of rebuilding its copy/subprocess/cleanup orchestration. Adequate project
audits and simpler valid substitutions take precedence; unsupported layouts need
project facilities. Capture each phase's exit and inspect actual failures. Check
copied imports and caller bindings in the test/probe process where practical;
separate import-only processes do not prove what tests load. Inspect helper source
when trust review, adaptation or troubleshooting requires it.

If tests survive, verify the same stronger assertion on correct and faulty code:
pass the former, fail the latter for the intended effect, not merely success or
container size. If killed, identify the detecting assertion or warning policy;
this protects that fault, not every lifecycle path.

## Deliver and stop

Give decisive commands/results and the gap/proposed assertion or detecting check.
Keep a harness/report only for requested reuse or delivery. Without isolated
execution, label the concern static. Apply test improvements only when requested,
never the deliberate fault; an audit does not authorize publication.

Stop when the scoped claim is assessed and requested improvements are verified. Try another fault only for a distinct boundary material to that claim; don't fish for survivors, chase a global mutation score, or remove every mock.
