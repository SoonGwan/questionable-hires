# Python audit: bring the fault, not the plumbing

Use the project's existing interpreter and actual installed skill path. Pass JSON on stdin: no recipe file or wrapper script is needed. This CLI is the normal interface; inspect implementation when review or troubleshooting requires it. Choose the actual task files and fault, not the example blindly.

```sh
/path/to/project/python /path/to/con-artist/scripts/audit.py --spec - <<'JSON'
{
  "files": ["service.py", "test_service.py"],
  "imports": ["service", "test_service"],
  "target": "service.py",
  "old": "    store.append(record)\n",
  "new": "",
  "runner": "unittest",
  "tests": ["-v", "test_service"],
  "probe": "from service import save\ns = ['existing']\nsave(s, 'record')\nassert s == ['existing', 'record']\n"
}
JSON
```

`files` selects relative files/directories including needed configuration. `imports` must include the affected implementation and resolve inside each copy. `old` must match `target` exactly once. `tests` supplies arguments for unittest or already-installed pytest. Optional `probe` is the same stronger assertion code for correct/faulty versions, not a replacement implementation. Omit it when only checking existing protection.

When the stronger probe is needed **only if existing tests miss the fault**, add `"probe_when": "survives"`. This runs correct/mutant tests first and runs both fresh-copy probes only if mutant tests exit 0. A nonzero mutant exit skips both probes and records `probe_skipped`; inspect its failure, do not automatically call it a killed behavioral fault or claim the proposed probe was validated. Omit this option (default `"always"`) when the probe itself must be verified regardless of existing coverage. A timeout or failing correct check still stops as incomplete.

For small, permitted package/test directories, select those directories plus required configuration rather than reconstructing their import dependencies file by file merely to minimize copy size. Directory selection preserves fixtures and support modules. Narrow the selection when size, scope, sensitive data or incompatible contents require it; do not copy a repository root, environment or unrelated data indiscriminately. The helper enforces its 20 MB input limit before execution.

Each check gets a fresh project-local disposable copy with verified imports. The copy is its working directory; listed imports run before tests or probe. A probe executes as `__main__` in that same process. For fixture-dependent assertions, create a test inside the copy and invoke pytest with `raise SystemExit(pytest.main([...]))`: calling `pytest.main` without propagating its result can falsely report success. Probe-created files do not carry over to another check.

The CLI emits JSON with `status` (`observed` or `incomplete`) and `checks`. Check keys are `correct_tests`, `mutant_tests` and, when run, `correct_probe`, `mutant_probe`. Each contains `exit_code`, `timed_out`, `output`, and `output_truncated`. Inspect the actual failure in `output`; neither `observed` nor a nonzero mutant exit establishes coverage. `probe_skipped`, when present, explains unvalidated conditional probes; absent checks are not passes.

Correct-code failure or timeout stops as incomplete. CLI exit 0 means observations collected; exit 2 means invalid/incomplete evidence (invalid input may produce only stderr). Selected original bytes are checked and copies removed. Output retains a 12,000-character tail per check; invalid UTF-8 is replaced. Timeout defaults to 30 seconds per check; `--timeout` allows at most 300.

Limits: POSIX, Python 3.9+, 20 MB selected inputs; no symlinks/Git internals/path traversal or namespace-package import checks. No dependency installation. This is **not a sandbox**: use trusted tests, local data and authorized actions only. Files outside the selection are not integrity-checked or restored. Use normal project facilities for other languages or unsupported layouts; don't repeat a valid baseline merely to adopt this helper mid-audit.

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
not another execution or independent observation. Incomplete evidence stops the
batch; unrun entries are not passes. This saves repeated baseline execution,
not the reasoning needed to select faults or interpret failures.
