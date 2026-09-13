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
accepts shared `files`, `imports`, `runner`, `tests` plus a `mutations` list
(1–8 objects). Move each fault's `target`, `old`, `new`, optional `probe` (or
`probe_files`/`probe_tests`) and
`probe_when` into its own list entry; no other per-fault overrides are supported.
Use this only for distinct boundaries already needed by the audit, not to
generate extra faults or batch an investigation whose next step depends on results.

Within that invocation, a successful normal test result is reused when selected
bytes/modes, imports, test arguments, interpreter, timeout and environment match.
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
