# Optional Python audit modes

Read only the section needed by the current audit; the common CLI and limits are in [Python audit](python-audit.md).

## Stronger probes

The [native-probe interface](python-audit-probes.md) now has its own short guide.
Read it for `probe_files`/`probe_tests` and conditional stronger assertions; the
other sections here are not prerequisites. This heading preserves existing links.

## Several already-justified faults, one baseline

Read the [batch guide](python-audit-batch.md) for shared setup, test-selection
entries, baseline reuse and partial failures. This heading preserves older links.

## Copied import roots

When the project's evidenced runner uses a source directory such as `src/`, add
`"import_roots": ["src"]` to the recipe and select the required source files in
`files`. The helper prepends these directories **inside each disposable copy**,
in listed order, followed by the copy root. Default `[]` keeps the existing
root-only behavior. This path setup precedes listed imports, prechecks, tests and
probes; it never points at the original source or installs a package.

Roots must be distinct project-relative directories containing selected files.
Absolute paths, traversal, the already-added `.` root, symlinks, missing/empty
selections and duplicate normalized paths are rejected before test execution.
Keep required package initializers and configuration in the selection. Listed
imports must still resolve to files inside the copy; inspect their reported
paths and caller bindings. Root order can change which same-named package wins
and is part of baseline-reuse identity. Batch mode shares roots across faults.

Use the project's documented path order, not a guessed path that hides an import
failure. Explicit source roots do not reproduce editable-install hooks, build
steps, package metadata, compiled extensions or namespace-package validation.
Use project facilities when those are required. The helper still removes inherited
PYTHONPATH, so unrelated ambient source trees cannot serve as an implicit recipe.

## Native unittest module invocation

Use `"invocation": "module"` only when the required runner is
`python -B -m unittest <tests...>`. Default `"bootstrap"` remains unchanged;
pytest and inline `probe` code cannot use module mode. For stronger assertions,
use `probe_files` or `probe_replacements` with `probe_tests`. Batch mode shares
`invocation`, and changing it invalidates reusable baselines.

The child really executes `-m unittest` from its disposable copy. A temporary
startup adapter wraps `unittest.TestProgram.runTests` to verify copied imports
and the optional precheck after native test loading and before test execution,
then record the actual native result. This is instrumented execution, not an
untouched interpreter: it changes the method identity and installs copy-local
import roots. Use project facilities if uninstrumented startup, custom runner
internals, or exact method identity are required. Import evidence does not prove
later function bindings; retain justified same-process prechecks.

Interpreter site/user customization runs before checked imports; disabled user
site remains disabled. The adapter removes itself from import lookup and child
environment inheritance. Selected project-local `sitecustomize`/`usercustomize`
modules are rejected rather than replaced. No package installation is performed.

Each executed check adds `command`, `invocation`, `native_exit_code` and
`suite_observation` (`tests`, `skipped`, `successful`). Ordinary pass/failure keeps
the native exit. A successful empty/all-skipped suite maps to check exit 5;
missing/invalid completed-suite evidence maps to 7, including help-only and early
zero exits. Disagreement between native exit success and the completed suite's
`successful` value also maps to7, with `incomplete_reason`; shutdown behavior
must not turn a failed suite into a passing baseline or a passing suite into
fault-detection evidence. Timeouts stay timeouts. The original native exit and captured output
remain available; import/precheck errors without a completed suite also map to 7.
These fields do not automatically classify assertion failures as detected faults.
Support runs inside the owned scratch tree and is removed with it. This is not a
sandbox or protection against tests deliberately forging observation files.

## Diagnostics and incomplete evidence

Input collection bounds each read to the remaining 20 MB selection budget plus
one overflow-detection byte and charges actual bytes, including growth after the
size check. This bounds the collected input payload, not total process memory or
filesystem races. The final original-file comparison rejects changed size/mode
before reading and bounds equal-size reads to the original length plus one byte.
Neither check makes concurrent source changes a stable snapshot or restores files.

Use this section when a check reports incomplete evidence, unexpected runner
errors/warnings or cleanup failure. Ordinary successful checks use the common
CLI contract; helper implementation review remains appropriate for trust review,
adaptation or unresolved behavior, not a prerequisite to construct a recipe.

### Prechecks

Listed-import setup runs before prechecks. Import exceptions, copy-location
verification failures and early SystemExit (including zero) are labeled
`Import setup failed; not mutation evidence` and use reserved check exit 7.
They stop either correct or mutant execution as incomplete, before subsequent
probes or batch faults. Original exception text remains in the captured output.
A probe/test that independently exits 7 is conservatively incomplete too; do not
use that reserved exit to claim detection. This catches ordinary Python exits,
not hostile low-level termination such as os._exit, nor later runner early exits.
The helper is not a security sandbox; inspect actual native test evidence.

Prechecks share each check's timeout/output limit. Exceptions are labeled
`Precheck failed; not mutation evidence`. With a precheck enabled, check exit 6
is reserved for incomplete precheck evidence and stops even a mutant audit.
Early `SystemExit(0)` also counts as incomplete. Do not replace behavior to make
a precheck pass. Batch precheck is shared; changing it invalidates reusable
baselines. It verifies bindings at that point, not later fixture behavior.

### Empty suites and assertion plumbing

Normally completed unittest runs with zero tests or only skipped tests have check
exit 5 and an explicit diagnostic. An empty correct suite or native correct probe
stops as incomplete, not a reusable baseline. Actual failures retain exit 1.
Exit 5 stops correct and mutant checks, including native probes and batches, as
incomplete. A mutant that removes collection or skips every test did not establish
detection; it must not trigger the conditional-probe skip path. Inline code that
explicitly exits 5 is conservatively incomplete too, not a killed fault.
Inline assertion probes are not unittest suites and remain supported; pytest
retains native exits. Help/early exits or nonzero mutant exits do not prove actual
test execution or a killed behavioral fault.

A helper overriding `unittest.TestCase.fail` can break assertion handling:
an incompatible signature gives TypeError; an async override accepting the message
can return an unawaited coroutine and let a mismatch pass. Inspect warnings and
helper definitions. A stronger probe needs a working failure path of its own;
do not copy a broken assertion helper into it. Native outputs/exits do not
automatically classify production versus test defects. Do not repair the original
suite or change warning policy merely to credit a kill.

### Cleanup and interruption

Required test/probe work must finish in the foreground. When the direct runner
exits, remaining process-group members are killed and buffered output drained
under the original deadline; inherited pipes no longer force a finished check
to time out. Exit detection polls every 50 ms, subject to scheduling. Background
jobs intended to survive the runner are unsupported; escaped groups are not
contained. Tests still own assertions and orderly cleanup.

Child-exit confirmation has a separate five-second cleanup wait. An unconfirmed
exit stops the audit/batch with CLI exit 2 and an audit-not-established error,
not collected evidence. Existing interruptions/errors propagate. This is not an
OS termination or descendant-containment guarantee; do not automatically retry
while the previous process may remain. Selected original bytes/modes are checked;
changes are reported, never silently restored. Files outside selection are not
integrity-checked or restored.
