# Import setup is not a passing test

## Reproduced defect

At `d2a5ccd`, a selected implementation containing `raise SystemExit(0)` during
import caused the audit to return `status: observed` with zero child exits despite
never reaching native tests. A mutation introducing that import-time exit also
looked like survival and scheduled stronger probes that exited before assertions.
Two new author regressions reproduced both incorrect statuses: 73 focused tests
ran in 11.913s with exactly those two failures.

This is a helper false-green path on an authored fixture, not a finding that a
previous model benchmark actually encountered it. Historical logs and metrics
remain unchanged; no original model evidence is retroactively repaired.

## Correction and limits

Listed imports and copy-location verification now catch Python exceptions and
early exits, retain their traceback and exit with reserved check code 7. Either
correct or mutant setup failure stops as incomplete, before further probes or
batch faults. A normal import still reaches the unchanged native runner. This
adds no subprocess or extra source scan.

Import-time syntax failures now also stop as incomplete rather than returning
observations with only a general caution. Two existing syntax tests consequently
need the stronger expected status; the first post-change focused run still had
one old expectation and failed (73 tests, 14.557s). That expectation was corrected,
not the mutation or required rejection behavior.

Reserved exit 7 from a custom runner/probe is conservatively incomplete too.
This is not a sandbox or universal execution-attestation protocol: os._exit,
hostile process behavior and later runner early exits remain outside this narrow
correction. Actual native assertion output still matters.

## Author validation

After correcting the old expectation and adding src-package CLI and batch-stop
controls, all **75 focused tests passed in 15.041s**. Tests exercise zero/nonzero
SystemExit during src package initialization, CLI exit 2 with captured import
failure, intact originals/cleanup, mutant setup stopping conditional probes and
subsequent batch faults, and native assertion outcomes on valid imports.

No model timing took place during these edits. The established improvement is
rejection of a demonstrated unexecuted-test success path, not token savings or
all-eight completion.

## Downstream compatibility

The first full run (405 tests, 67.441s) exposed the old conditional-syntax
expectation already loaded before its correction, plus a report-generator test
expecting execution to continue after import-time syntax failure. Neither is
ignored. The prospective generator now emits a distinct
`con-artist-report-reference-v2` task, with both valid behavioral mutations before
the final syntax failure and an explicit incomplete-import criterion. Its focused
test passed in 0.318s. Frozen prior case files, measured reports and original
criteria are unchanged; no new model comparison was launched from this generator.

Final full run: **405 tests passed in 65.072s**. Repository links/metadata, skill
validation, featured-language synchronization and diff whitespace checks passed.
