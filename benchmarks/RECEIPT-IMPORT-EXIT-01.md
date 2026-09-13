# Receipt import-exit evidence correction

Native author regression, not model performance evidence. Starting repository
revision `dfaca19`. Historical benchmark inputs, captures and scores are unchanged.

The existing comparison bootstrap imported listed implementation modules before
entering unittest/pytest. A module raising `SystemExit(0)` therefore returned a
successful check without executing regression assertions. Other import exceptions
also left the comparison `observed` and allowed the next variant to execute.
Receipt already required reviewing assertions, but its execution classification
could misleadingly resemble completed comparison evidence.

An added real Git-fixture regression exercised import-time `SystemExit(0)`,
`SystemExit(9)` and `RuntimeError`. All three subcases failed against the previous
helper: actual `observed`, expected `incomplete` (41 tests, 14.771 seconds).

The bootstrap now catches ordinary Python exceptions/exits only around listed
imports and copied-location validation, retains traceback and reserves check exit
7. The comparison records the check, marks itself incomplete, skips the next
variant, performs original-file integrity checks and removes its owned copies.
CLI returns 2. A native runner independently returning 7 is conservatively treated
as incomplete as well. External-import provenance failures follow this path.

The same regression suite then passed: 41 tests, 14.616 seconds. A subsequent CLI
regression covers the other direction: a genuine assertion failure before the fix,
followed by an uncommitted implementation that exits 0 during import. The before
assertion remains visible; the after check must record exit 7 and `SystemExit: 0`,
without claiming test execution. CLI must be 2 and cleanup/integrity must hold.
The final full repository suite passed all 409 tests in 65.297 seconds, including
that CLI regression and existing successful before/after comparisons. Skill,
metadata/link, featured synchronization and whitespace checks also passed.

This is not a sandbox or general test-run attestation: `os._exit`, native process
termination and later runner early exits are not caught by this import guard.
Do not interpret reserved status or green tests as complete requested coverage.
No percentage speedup or new featured chart is claimed; skipping a comparison
after invalid setup is valid stopping behavior, not equal-work model efficiency.
