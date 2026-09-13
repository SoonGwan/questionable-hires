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

For pytest, list implementation modules in `imports`, not selected test modules:
pre-importing tests bypasses pytest's assertion rewriting and can lose useful
expected/observed diagnostics. Let pytest collect its tests normally.

For native fixture-based assertions, use `probe_files`/`probe_tests` from
[probe execution](python-audit-advanced.md#stronger-probes), avoiding nested Python
strings; that section also covers conditional execution. For several already-justified
faults with one reusable baseline, read [batch mode](python-audit-advanced.md#several-already-justified-faults-one-baseline).
Neither mode is needed just to assess one existing test against one fault.

For small, permitted package/test directories, select those directories plus required configuration rather than reconstructing their import dependencies file by file merely to minimize copy size. Directory selection preserves fixtures and support modules. Narrow the selection when size, scope, sensitive data or incompatible contents require it; do not copy a repository root, environment or unrelated data indiscriminately. The helper enforces its 20 MB input limit before execution.

Each executed check gets a fresh project-local disposable copy with verified imports and the copy as its working directory. Batch mode can reuse successful correct-code observations as documented above. Listed imports execute before the selected test runner.

The single-audit CLI emits JSON with `status` (`observed` or `incomplete`) and `checks`. Check keys are `correct_tests`, `mutant_tests` and, when run, `correct_probe`, `mutant_probe`. Each contains `exit_code`, `timed_out`, `output`, and `output_truncated`. Batch reuse references an earlier observation instead of duplicating its output, as described in batch mode. Inspect the actual failure in `output`; neither `observed` nor a nonzero mutant exit establishes coverage. `probe_skipped`, when present, explains unvalidated conditional probes; absent checks are not passes.

Correct-code failure or timeout stops as incomplete. CLI exit 0 means observations collected; exit 2 means invalid/incomplete evidence (invalid input may produce only stderr). Selected original bytes and permission bits are checked and copies removed; detected original changes are reported, never silently restored. Output retains a 12,000-character tail per check; invalid UTF-8 is replaced. Timeout defaults to 30 seconds per check; `--timeout` allows at most 300.

Normally completed unittest runs with zero tests or only skipped tests have check
exit 5 and an explicit diagnostic. An empty correct suite or native correct probe
therefore stops as incomplete, not a reusable baseline. Actual failures retain
exit 1. Inline assertion probes are not unittest suites and remain supported;
pytest retains native exits. Help/early exits or a nonzero mutant exit still do
not prove execution or a killed fault: inspect the actual tests and assertions.

Child-exit confirmation has a separate five-second cleanup wait. An unconfirmed exit stops the audit/batch and produces CLI exit 2 with an audit-not-established error, not collected evidence. Existing interruptions/errors propagate. This is not an OS termination or descendant-containment guarantee; do not automatically retry while the previous process may remain.

Limits: POSIX, Python 3.9+, 20 MB selected inputs; no symlinks/Git internals/path traversal or namespace-package import checks. No dependency installation. This is **not a sandbox**: use trusted tests, local data and authorized actions only. Files outside the selection are not integrity-checked or restored. Use normal project facilities for other languages or unsupported layouts; don't repeat a valid baseline merely to adopt this helper mid-audit.
