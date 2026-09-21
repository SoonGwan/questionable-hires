---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Trace the requested assertions far enough to establish the actual exercised effect
and select a reachable fault. Follow unresolved bindings, mocks and relevant setup;
reading every intermediate wrapper is not itself evidence. Reuse known instructions,
runner and source context. Keep discovery inside the permitted project root; a
broad suite need not become a reading list of unrelated tests.

Use the evidenced runner and configuration; reuse a valid correct-code baseline.
Choose one meaningful fault at the requested boundary, such as acknowledging
without persisting. Preserve originals and compilation/binding context through
project isolation, disposable module/package copies or a valid substitution;
restore substitutions in reused processes. A wrong binding, rewritten simulation,
syntax error or equivalent mutation cannot establish test sensitivity.

Inspect each phase's actual assertion and exit, not just a green baseline or a
nonzero mutant status. Runner errors/warnings can indicate broken assertion
plumbing, not a detected production fault. Establish provenance through copied
imports, traced bindings and defect-specific observations. Add instrumentation for
required or unresolved dispatch, not duplicate evidence; a separate import-only
process does not prove what the test process loads.

## Use support only where it helps

- Nearby known files: read relevant source/configuration directly. For scattered
  Python context, [the collector](references/python-context.md) locates definitions,
  ancestor instructions and fixtures. Select known bodies directly; indexes are
  navigation, not reviewed bodies or execution. Don't recollect equivalent context.
- Existing Python test improvements: consider [the complete four-check recipe](references/existing-tests.md)
  when they remove custom copy/run/cleanup plumbing. One recipe checks original
  and proposed tests against correct/faulty code with the native runner and fixtures;
  applying the verified edit remains separate. No helper is needed for a simpler
  native workflow or an already-completed audit.
- Small self-contained audits: use the native runner in project-local copies or
  a valid substitution. Choose [the Python helper](references/python-audit.md) when
  its bounded processes, selected-input integrity checks or shared-baseline batches
  remove needed orchestration. Python compatibility alone is not a reason to adopt
  it or load its guide. Read implementation for a concrete trust/adaptation question.
- Unexpected Python runner errors/warnings: [diagnostics](references/python-audit-advanced.md#diagnostics-and-incomplete-evidence)
  covers false-pass assertion helpers and incomplete checks. It is not routine setup.

If tests survive, verify the same stronger assertion on correct and faulty code:
pass the former, fail the latter for the intended effect, not merely success or
container size. Assert the requested behavioral contract; extra constraints on
incidental representation or object identity can reject valid implementations.
Keep identity/order checks when they are part of that contract. If killed,
identify the detecting assertion or warning policy;
this protects that fault, not every lifecycle path.

## Deliver and stop

Give decisive commands/results and the gap/proposed assertion or detecting check.
Keep a harness/report only for requested reuse or delivery. Without isolated
execution, label the concern static. Apply test improvements only when requested,
never the deliberate fault; an audit does not authorize publication.

Stop when the scoped claim and requested improvements are verified. Add faults
only for distinct material boundaries, not to fish for survivors, chase a global
mutation score or remove every mock. Preserve user changes and explicit requirements.
