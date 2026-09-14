# Final-check batching — a lower-round-trip candidate

Subsequent [model adoption screen](HOSTAGE-FINAL-BATCH-MODEL-01-REVIEW.md)
records actual batching with a partial original test transcript; this local
preflight remains separate evidence, not a retroactive model-performance result.

2026-09-14. The [keyed-import model at `6d0d108`](HOSTAGE-KEYED-IMPORT-01-REVIEW.md)
used separate commands for native tests (item 7), copy/original-test checks
(item 9), and final diff/status (item 10). Those final two commands use semicolons:
their final success alone cannot establish every earlier check's exit. The
original bytes and successful test transcript were separately reconciled; do
not retroactively invent a failed original check.

The Hostage entry now says to group remaining native tests, copy-integrity and
diff/status checks when no intervening decision is needed. It distinguishes
failure-preserving `&&` from a requirement to run all checks and retain separate
statuses. Existing helper copies must not be recopied just to hide mismatches.
This replaces the less specific final-check paragraph; no new runtime/helper,
universal shell workflow, extra reference read or new test requirement is added.

## Actual native preflight

`tests/test_hostage_final_batch.py` uses the six retained keyed-import tests,
actual `cmp`, actual temporary Git repositories and project-local scratch. It
compares these checks in a single shell invocation:

```text
native tests && cmp(source, copy) && unchanged-original-test diff
  && whitespace diff check && scoped diff && status
```

The project interpreter and quoted file paths are used; one source filename has
a space. All checks run successfully for the unmodified project. Four deliberate
faults each produce nonzero batch status: broken production cleanup, changed
helper-copy bytes, edited original test, and trailing whitespace. Tests still
run six cases; copy/original/whitespace faults do not alter their application
behavior. The same commands joined with semicolons return zero after successful
final status despite the earlier failure. Nothing repairs or overwrites the
selected files, and all contents remain unchanged after each check.

Initial author-check error is preserved here: the copy-fault assertion expected
`controlled_call.py` in output, but macOS cmp reported `EOF on .../source asset.py`.
The first unittest run had one failing subtest (copy) in 1.313s. This was an
incorrect diagnostic-format assumption, not failure of cmp to detect the edit.
The corrected assertion checks failed comparison status and cmp diagnostic after
passing native tests, without requiring the second filename. Native failures
must be inspected, not inferred from a guessed message format.
Corrected targeted test: passes all five scenarios in 1.795s. Full repository
validation: 502 tests pass in 75.145s, no failures/skips; skill/catalog validation,
diff checks and featured EN/KO synchronization pass. This is local validation.

## Limits

This is executable support for an instruction candidate, **not** model adoption
or a token/time result. Combining three shell calls is possible for the observed
finalization sequence; it does not remove the underlying required commands or
prove a percentage saving. Test failures still require decisions and later checks
may remain unrun. Some workflows need per-check statuses instead. No need to
repeat already-valid evidence or schedule extra checks just to fill a batch.

No model run or featured image changes in this correction. The skill-creator
principle used here is a narrow change supported by observed behavior, preserving
scope and necessary checks instead of accumulating a new helper API.
