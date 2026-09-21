# Repeated native unittest checks

Use this optional recipe when independent, already-required faults need copied
native execution and shared baseline evidence. Existing project support or a
simple direct check may be sufficient. This is not a reason to add faults.
Adapt complete selected files, reachable edits and the test binding to the project;
do not extract a function when that loses its imports, closures or decorators.

Run with the project interpreter and installed skill path; send JSON on stdin:

```sh
/path/to/project/python /path/to/con-artist/scripts/audit.py --source . --spec - <<'JSON'
{
  "files": ["service.py", "test_service.py"],
  "imports": ["service", "test_service"],
  "runner": "unittest",
  "invocation": "module",
  "tests": ["test_service.SaveTests.test_acknowledges_save", "-v"],
  "precheck": "import service, test_service\nassert test_service.SaveTests.test_acknowledges_save.__globals__['save'] is service.save\nprint('Verified native test save binding', flush=True)\n",
  "mutations": [
    {"target": "service.py", "old": "    store.append(record)\n", "new": ""},
    {"target": "service.py", "old": "    store.append(record)\n", "new": "    store.extend([record, record])\n"}
  ]
}
JSON
```

Select existing relative files/directories plus required fixtures/configuration.
For an evidenced `src/` layout, select those source files and add shared
`"import_roots": ["src"]`. Roots are distinct relative directories containing
selected files, searched inside each copy before its root; include package
initializers. This does not install packages or reproduce editable/build hooks.
Each `old` must match its selected `target` exactly once. The shared recipe accepts
1–8 independent mutations; an entry may override `tests` for required test-specific
process exits. Use a suite when its native method results suffice; separate exits
require separate selections. Do not batch steps whose next action depends on results.

Each executed check runs `python -B -m unittest <tests...>` in a fresh project-local
copy. Listed imports must resolve inside it. Optional `precheck` verifies a required
or unresolved binding in that test process after loading and before execution;
it does not prove later rebinding, call counts or behavioral effects. An internal
startup adapter observes the real runner; you need not write your own hook.
Interpreter hooks are preserved, but selected project startup customization is
rejected, not overwritten. Method identity/startup is instrumented, not untouched.
Use project facilities for incompatible startup or custom runner requirements.

Read ordered `audits[*].checks.correct_tests` and `mutant_tests`, actual native
counts/assertions, `exit_code`, `timed_out` and `output_truncated`. A repeated normal
selection may contain `observation_ref` pointing to its one earlier execution;
resolve that reference instead of counting another run. Reuse requires matching
source bytes/modes, configuration and environment within this batch. Every mutant
executes. External state/flakiness is not controlled; use fresh observations when
the contract requires them. No cache survives another CLI invocation.

`command`, `native_exit_code` and `suite_observation` retain module-mode evidence.
Empty/all-skipped suites map to check exit5; missing completed-suite evidence,
including setup failure/help-only/early zero exit, maps to7. CLI0 means observations
collected, not a killed fault; CLI2/`incomplete` means evidence is not established.
Timeouts, missing checks, setup errors and bare nonzero exits are not detection.
Inspect the intended assertion; a failed normal check stops later work.

The example checks existing protection only. If an existing unchanged test
already supplies a required stronger assertion, another mutation entry with the
same fault and different `tests` runs its correct/faulty pair; no probe fields are
needed. Include that test and its imports in the selected files and adapt any
binding precheck. The same observation/reuse rules apply. Only when adding or
changing assertions, use `probe_files`/`probe_replacements` and `probe_tests`:
see [native probe details](python-audit-probes.md). Module mode does not support
inline `probe` or pytest. Never call an unexecuted proposal verified.

`integrity` confirms selected original bytes/modes and owned-scratch removal.
For required whole-project preservation, add shared `"guard_project": true` only
when reading the entire project is authorized. Its before/after inventory covers
paths/bytes/modes and in-root Git metadata (10,000 entries/20 MB), not external
targets. Changes raise without restoring originals; this is not an atomic snapshot.

Limits: trusted local tests, Python3.9+/POSIX,20 MB selected inputs, no selected
symlinks/Git internals/traversal/namespace-package checks, no installation or sandbox.
Each check retains its last12,000 output characters; provenance can be truncated.
CLI `--python` selects an existing interpreter; `--timeout` sets seconds/check
(default30,max300), not JSON fields. Foreground work only; surviving background
jobs are unsupported. Do not retry an unconfirmed child exit. For import-root
edge cases or unresolved errors, consult [advanced details](python-audit-advanced.md).
This recipe covers native batches with existing tests; the common/probe guides
are not prerequisites for that path. Inspect implementation when a concrete
trust or adaptation question needs it. Do not rerun completed checks merely to
adopt this recipe.
