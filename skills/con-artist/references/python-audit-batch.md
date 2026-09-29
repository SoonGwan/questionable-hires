# Batch only the audit work already needed

Read with the [common CLI contract](python-audit.md). Batch mode does not require
loading unrelated import-root or runner-diagnostic details.

For independent, already-scoped local audits, the same CLI accepts shared `files`,
`imports`, `runner`, `tests`, optional `precheck` and `import_roots` plus a `mutations` list
(1–8 objects). Move each fault's `target`, `old`, `new`, optional `probe` (or
`probe_files`/`probe_replacements`/`probe_edits` with `probe_tests`) and
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
Returning to an earlier selection (A→B→A) reuses its original successful observation,
not only the immediately previous selection. One shared selected-input context is
retained for up to eight normal-result entries, not a source copy per selection.
Every audit still rereads/validates current inputs; any change to the shared identity,
including runner, invocation mode, precheck or optional project-guard state, clears those entries.
This does not cache failed checks, skip mutants or change requested audit order.
An identical stronger probe also reuses its successful correct-code observation
under those same conditions; changing the probe, new files or replacement contents
runs a new correct-code check.
Returning to an earlier identical probe also reuses its original observation.
Native file probes execute `probe_tests` instead of the original test arguments,
so changing only the original selection does not invalidate that probe result.
Its actual `probe_tests`, new/replacement bytes and all other shared inputs must
still match. Inline probes retain the original test arguments in their context.
Probe retention is limited to eight successful entries and20 MB of probe text/file
contents in total; oldest entries are evicted when needed. Eviction means a fresh
correct-code check, not missing evidence. These limits do not bound total process
memory, result logs or the shared input snapshot. Neither cache establishes external-state freshness.
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

On an ordinary input, execution or integrity failure, CLI exit 2 retains earlier
audits and any checks already returned by the failing audit, including baseline
references. Its incomplete entry may contain `execution_error` and/or
`integrity_error`. If that audit returned no checks, a later-audit failure instead
has `error` and empty `checks`; this does not prove nothing executed. With no
returned evidence anywhere, the CLI may emit only stderr.

The Python API keeps its existing distinction: later input/I/O failures return
an incomplete batch; `RuntimeError` and first-audit errors raise, attaching any
available partial batch as `error.audit_result`. Interruptions are not converted
to ordinary incomplete results. Remaining mutations are unrun. Inspect the error
and process state before retrying; do not discard returned evidence or infer
missing checks. See the [common result contract](python-audit.md) for guard fields.
