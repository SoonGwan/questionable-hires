# Receipt native unittest invocation — 2026-09-14

Previous source `587fb84`. The [SQLite transfer](RECEIPT-LEDGER-01-REVIEW.md) showed
both skill sessions inspecting and replacing helper internals to run the specified
`python -B -m unittest` command. Their combined token/time costs increased. This
candidate provides that execution mode directly; it does not change the frozen
tasks, old observations or the default bootstrap behavior.

## Supported operation

Optional recipe `"invocation":"module"`, with `runner: "unittest"` and existing
test arguments, launches `[python, '-B', '-m', 'unittest', *tests]`. The configured
interpreter is honored. A temporary copy-local startup probe checks selected
imports in the same process, then lets the actual unittest module run. Existing
source-layout roots, frozen inputs, whole-tree guard, timeout/process-group cleanup
and 12,000-character output capture are reused, not replaced by a caller adapter.

The [Python startup-hook documentation](https://docs.python.org/3/library/site.html)
describes automatic site initialization and how `-S` suppresses it. The probe only
accepts module startup, records readiness after imports, and removes its own path
from child inheritance. An interpreter launcher cannot supply readiness just by
importing the hook while launching another Python process.

Selected project site/user customization is rejected before execution; other
discoverable startup customization is rejected by the probe rather than silently
shadowed. Missing/skipped/failed provenance reserves check exit 7, stops the next
comparison and produces CLI 2; original native exit is retained separately.
No original file or installed/user startup configuration is rewritten. Probe files
exist only in owned comparison copies and are removed with those copies.

Module results include actual command, `native_exit_code`, `provenance_ready` and
unchanged native output fields. **Native empty/all-skipped unittest runs still
exit 0**; counts/skips and actual assertions must be reviewed. This is deliberately
different from the default bootstrap's check-5 empty/all-skipped guard. Neither
CLI 0 nor startup readiness proves the requested behavior. Native mode currently
supports unittest only; pytest continues using the existing bootstrap route.

## Actual validation

Final native suite: **13 tests / 6.227s**, including:

- Actual `-B -m unittest` process arguments, same-process copy imports, real before
  assertion failure/after success and unchanged whole tree.
- Both frozen SQLite cases through the literal native entry: complete fix passes,
  acknowledgement-only fix still fails on actual committed balances. Five tests
  per phase, source identity/import readiness, unchanged current inputs, clean DBs.
- Source-layout imports, empty/all-skipped native results, and `SystemExit(0)` in
  a selected import producing incomplete setup rather than a passing comparison.
- Shell and Python interpreter launchers disabling site initialization: native
  exit 0 cannot masquerade as successful provenance; no second comparison runs.
- Project startup hooks and a configured user-site hook are not silently replaced.
- Native timeout, output overflow and finished-runner/inherited-child-pipe handling.
- Copied standalone CLI outside the checkout, and invalid mode rejection.

Existing helper **47 / 15.328s**, tree guard **8 / 3.751s**, frozen ledger fixture
**2 / 0.779s**, packaging **12 / 3.294s** also pass: 82 related tests in total,
not a new full-bundle test count. Local Python 3.9.6 on macOS. Skill/repository
validation, featured EN/KO synchronization and whitespace checks pass.

## Costs and limits

Entry/discovery and resource count remain unchanged. Helper source grows
21,873 → 25,279 bytes (+3,406), guide 6,682 → 7,563 (+881). The extra startup
probe adds execution work; avoiding model-written adapters is a hypothesis until
another measured session actually uses it. No token/time saving is claimed yet.

Tests are trusted, and this remains **not a sandbox**. Startup instrumentation
pre-imports requested modules, configures child-local lookup and is not suitable
for required custom site/user hooks or disabled site initialization. Normal Python
site-package machinery is not isolated. The marker is operational evidence, not
tamper-proof attestation. Existing limits on escaped descendants, transient writes,
concurrency and whole-tree comparison intervals still apply.

Next screen must use the unchanged task obligations and inspect actual command
selection, absence/presence of internal adapters, native results, source identity,
cleanup and all resource costs. Preserve adverse outcomes and replay differences;
do not extrapolate from these local tests or change historical/featured charts.
