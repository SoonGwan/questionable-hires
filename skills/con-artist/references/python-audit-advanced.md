# Optional Python audit modes

Read only the section needed by the current audit; the common CLI and limits are in [Python audit](python-audit.md).

## Stronger probes

When the stronger probe is needed **only if existing tests miss the fault**, add `"probe_when": "survives"`. This runs correct/mutant tests first and runs both fresh-copy probes only if mutant tests exit 0. A nonzero mutant exit skips both probes and records `probe_skipped`; inspect its failure, do not automatically call it a killed behavioral fault or claim the proposed probe was validated. Omit this option (default `"always"`) when the probe itself must be verified regardless of existing coverage. A timeout or failing correct check still stops as incomplete.

Each check gets a fresh project-local disposable copy with verified imports. The copy is its working directory; listed imports run before tests or probe. A probe executes as `__main__` in that same process. For fixture-dependent assertions, create a test inside the copy and invoke pytest with `raise SystemExit(pytest.main([...]))`: calling `pytest.main` without propagating its result can falsely report success. Probe-created files do not carry over to another check.

## Several already-justified faults, one baseline

For deterministic local tests sharing the same inputs and command, the same CLI
accepts shared `files`, `imports`, `runner`, `tests` plus a `mutations` list
(1–8 objects). Move each fault's `target`, `old`, `new`, optional `probe` and
`probe_when` into its own list entry; no other per-fault overrides are supported.
Use this only for distinct boundaries already needed by the audit, not to
generate extra faults or batch an investigation whose next step depends on results.

Within that invocation, a successful normal test result is reused when selected
bytes/modes, imports, test arguments, interpreter, timeout and environment match.
Each mutant and each probe still runs in a fresh copy. Nothing is cached across
invocations. External services, changing dependencies, clock/random behavior and
flaky tests are not controlled: use separate audits when a fresh baseline matters.

Batch JSON contains `status` and ordered `audits`, each with the single-audit
structure above. `correct_tests_reused: true` explicitly marks a copied result,
not another execution or independent observation. Its `correct_tests` retains
`exit_code` and `timed_out`; `observation_ref` is a JSON Pointer to the earlier
complete check in the same response. Read that check's `output` and
`output_truncated` instead of expecting a second copy of the log. References
always point directly to an executed observation, never another reference.
Incomplete evidence stops the
batch; unrun entries are not passes. This saves repeated baseline execution,
not the reasoning needed to select faults or interpret failures.
