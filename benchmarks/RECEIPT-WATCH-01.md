# Receipt: remove repeated selected-original guard scaffolding

## Evidence and change

The [graph pair](results/receipt-graph-01/README.md) used the comparison helper
but still wrote a wrapper to hash/mode-check unrelated notes and report cleanup.
It also redirected global TMPDIR into the project; an `xcrun_db` file appeared,
requiring another command. That measured pair remains **+15.49% tokens / +28.15%
time**, with explicit limits. This change does not improve its historical scores.

The helper now accepts optional `watch` file/directory selections. These reuse
bounded snapshot reading and final integrity checks but **never enter either
comparison copy**. Watched leaves must be disjoint from fixed/vary selections;
the same symlink, canonical-path, traversal and shared byte-budget checks apply.
Existing recipes remain accepted. New result fields report selected original
SHA-256 values/modes, watch-only paths, unchanged status, and owned-copy removal.
Failure to preserve an original still raises without restoring user data.

Child TMPDIR/TMP/TEMP defaults now point to each comparison copy. The helper's
own environment is not changed. This localizes normal Python tempfile use without
requiring a wrapper to redirect Git/other launcher scratch into the source root.
It is **not** proof that it prevents every macOS launcher artifact. Test code can
override paths/environment; this remains trusted-test automation, not a sandbox.

The reference explains when the structured report replaces redundant checks and
when stronger requirements still need separate verification. This follows the
skill-creator principle of moving repeated deterministic mechanics into scripts,
not requiring the model to reconstruct them for each request.

## Checks

`tests/test_receipt_helper.py` adds:

- Real native before/after comparison with an unrelated watched file, asserting
  intended before AssertionError/after pass, absence of that file in each copy,
  actual Python tempfile creation inside the copy, reported hashes/modes and
  removed comparison directories.
- Deliberate watched-file content change, permission change and deletion during
  execution: each is detected, not restored, with owned temporary copies removed.
- Invalid type/path and overlap rejection before executing checks.

Focused suite: **40 tests pass, 12.056 seconds**. Skill/catalog validation and
featured localization consistency checks pass. These are author checks, not
model adoption or whole-task efficiency evidence.
Full repository suite: **349 tests pass, 49.379 seconds**, including packaging
and executable reference-command checks, with no resource edits during the run.

## Boundaries and next evidence

`watch` protects selected existing regular-file leaves, not new directory entries,
Git index/status/commits, arbitrary side effects or concurrent-write atomicity.
The result's cleanup flag describes owned copies only. A successful outer CLI
still means observations collected, not proven regression coverage; inspect
both native assertions, provenance, timeout and output-truncation fields.

Further model confirmation needs an unexposed task and equivalent requested
outcomes. Do not rerun the exposed graph task to optimize its score or equate
removing Python wrapper code with measured token/time savings. All eight skills'
real-development performance goal remains active and unproven; featured graphs
and prior unfavorable results remain unchanged.
