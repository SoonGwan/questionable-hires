# Optional stronger probes only after test survival

Helper/reference revision `941ea50`. The character, entrypoint and default
behavior remain unchanged. When a recipe supplies a proposed stronger assertion
but needs it only if existing tests miss the fault, `probe_when: survives` checks
correct/mutant tests first. A nonzero mutant test exit skips both proposed-probe
runs, with an explicit `probe_skipped` reason. The probe is not then validated.

This is not an automatic coverage decision: syntax/import failures can also exit
nonzero. The caller must inspect the existing-test failure. Timeouts and failing
correct checks remain incomplete, not successful skips. With a surviving mutant,
the identical stronger probe still runs against separate fresh correct/mutant
copies. With default `always`, the previous execution order and all four checks
are preserved. Never use the conditional mode when the task independently asks
to validate the proposed probe itself.

## Deterministic checks

Six new helper tests cover detection with no probe execution, survivor execution
and copy independence, syntax-error non-certification, failed correct probe,
invalid condition inputs and mutant timeout. Existing default behavior, original
preservation, cleanup, import provenance, output limits and permission-mode tests
continue to pass: 24 helper tests total. The full local suite passes 98 tests;
all eight skill metadata/link sets and Con Artist skill validation also pass.

The retained [HTTPX recipe](con-artist-conditional-audit.json) uses the previously
pinned upstream checkout and interpreter, no network or dependency changes.
It mutates the default application-exception policy, with an optional actual
ASGI client probe. An author-run comparison invokes the helper directly with the
same recipe except `probe_when`; no model sessions or token benchmark were run.

| Mode | Executed checks/copies | Existing tests | Proposed probe | Single local seconds |
| --- | ---: | --- | --- | ---: |
| always | 4 | correct: 24 pass; mutant: 4 fail / 20 pass | correct pass; mutant expected assertion failure | 1.065 |
| survives | 2 | correct: 24 pass; mutant: 4 fail / 20 pass | explicitly not executed/validated | 0.720 |

Both mutant test outputs contain `DID NOT RAISE`; the always-mode mutant probe
reports suppressed application error. Both runs leave pinned upstream clean and
remove only their generated disposable copies. This establishes two avoided
process/copy operations in this conditional workflow, not a reliable speed ratio.

Crucially, previous model audits of this HTTPX fault already omitted an unnecessary
probe and used two checks. The comparison above is **not** an improvement over
those observed runs or over a no-skill baseline. The new option supports an
up-front conditional proposal without reimplementing scheduling; it is not an
excuse to attach gratuitous probes. Model routing/token benefit remains untested.

Keep this an optional mechanical improvement. No full-team claim, new superiority
chart, or rerun of an unchanged model workload is justified by these local numbers.
