# Batch only the audit work already needed

Read with the [common CLI contract](python-audit.md). Batch mode does not require
loading unrelated import-root or runner-diagnostic details.

For independent, already-scoped local audits, the same CLI accepts shared `files`,
`imports`, `runner`, `tests`, optional `precheck` and `import_roots` plus a `mutations` list
(1–8 objects). Move each fault's `target`, `old`, `new`, optional `probe` (or
`probe_files`/`probe_tests`) and
`probe_when` into its own list entry. An entry may also override `tests` with native
runner arguments when the audit requires separate test selections. Other per-entry
overrides are unsupported.
Use this only for distinct boundaries already needed by the audit, not to
generate extra faults or batch an investigation whose next step depends on results.

When distinct test-specific exits are required, keep the common recipe once and
put the same fault with each required `tests` selection in `mutations`. This batches
submission, not test execution: each selection still gets correct/faulty checks
in separate copies. Different test arguments invalidate baseline reuse. Do not add
both suite and individual runs unless the requested evidence needs both; a single
suite invocation already supplies its own assertion results, but not separate
per-test process exits. All selected tests and failure diagnostics remain necessary.

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
