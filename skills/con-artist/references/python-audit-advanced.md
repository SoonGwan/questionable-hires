# Optional Python audit modes

Read only the section needed by the current audit; the common CLI and limits are in [Python audit](python-audit.md).

## Stronger probes

For fixture-dependent pytest/unittest checks, prefer native test files rather than
embedding their source inside a Python `write_text` string inside JSON. Supply
`probe_files` (new relative file paths → source text) and `probe_tests` (arguments
for the same runner), **instead of** `probe`. For example, with `runner: "pytest"`:

```json
{
  "probe_files": {
    "tests/test_persistence_audit.py": "from service import save\n\ndef test_persisted():\n    store = []\n    save(store, b'\\xff')\n    assert store == [b'\\xff']\n"
  },
  "probe_tests": ["-q", "tests/test_persistence_audit.py"],
  "probe_when": "survives"
}
```

These fields augment the common recipe. Files exist only in the fresh
correct/faulty **probe** copies, never during the original-test checks or in the
source project. Existing project paths, selected-file collisions and traversal
are refused before execution. Inputs plus probe files share the 20 MB limit.
Native runner exit status is preserved automatically, including collection errors;
check actual assertion output. Normal single-layer JSON escaping still applies.
Batch probe reuse includes both file contents and probe test arguments.

When the stronger probe is needed **only if existing tests miss the fault**, add `"probe_when": "survives"`. This runs correct/mutant tests first and runs both fresh-copy probes only if mutant tests exit 0. A nonzero mutant exit skips both probes and records `probe_skipped`; inspect its failure, do not automatically call it a killed behavioral fault or claim the proposed probe was validated. Omit this option (default `"always"`) when the probe itself must be verified regardless of existing coverage. A timeout or failing correct check still stops as incomplete.

Each executed check gets a fresh project-local disposable copy with verified imports; batch reuse is described below. The copy is its working directory; listed imports run before tests or probe. A probe executes as `__main__` in that same process. For fixture-dependent assertions, create a test inside the copy and invoke pytest with `raise SystemExit(pytest.main([...]))`: calling `pytest.main` without propagating its result can falsely report success. Probe-created files do not carry over to another check.

## Several already-justified faults, one baseline

For deterministic local tests sharing the same inputs and command, the same CLI
accepts shared `files`, `imports`, `runner`, `tests`, optional `import_roots` plus a `mutations` list
(1–8 objects). Move each fault's `target`, `old`, `new`, optional `probe` (or
`probe_files`/`probe_tests`) and
`probe_when` into its own list entry; no other per-fault overrides are supported.
Use this only for distinct boundaries already needed by the audit, not to
generate extra faults or batch an investigation whose next step depends on results.

Within that invocation, a successful normal test result is reused when selected
bytes/modes, imports, ordered import roots, test arguments, interpreter, timeout and environment match.
An identical stronger probe also reuses its successful correct-code observation
under those same conditions; changing the probe runs a new correct-code check.
Each mutant test and mutant probe still runs in a fresh copy, as does every
non-reused correct check. Nothing is cached across
invocations. External services, changing dependencies, clock/random behavior and
flaky tests are not controlled: use separate audits when a fresh baseline matters.

Batch JSON contains `status` and ordered `audits`, each with the single-audit
structure above. `correct_tests_reused: true` or `correct_probe_reused: true`
explicitly marks a reused result, not another execution or independent observation.
The corresponding `correct_tests` or `correct_probe` retains
`exit_code` and `timed_out`; `observation_ref` is a JSON Pointer to the earlier
complete check in the same response. Read that check's `output` and
`output_truncated` instead of expecting a second copy of the log. References
always point directly to an executed observation, never another reference.
Incomplete evidence stops the
batch; unrun entries are not passes. This saves repeated baseline execution,
not the reasoning needed to select faults or interpret failures.

If a later audit raises an input/file error after earlier audits returned, CLI
exit 2 includes those earlier observations and a final `incomplete` entry with
`error` and empty `checks`. That entry has no usable checks; it does not prove
that nothing executed before the error. Remaining mutations are unrun. Inspect
the error and process state before retrying; do not discard completed evidence.
Errors before any returned audit, original-integrity/cleanup `RuntimeError`s and
interruptions still propagate without a collected batch report.

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

## Diagnostics and incomplete evidence

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

Child-exit confirmation has a separate five-second cleanup wait. An unconfirmed
exit stops the audit/batch with CLI exit 2 and an audit-not-established error,
not collected evidence. Existing interruptions/errors propagate. This is not an
OS termination or descendant-containment guarantee; do not automatically retry
while the previous process may remain. Selected original bytes/modes are checked;
changes are reported, never silently restored. Files outside selection are not
integrity-checked or restored.
