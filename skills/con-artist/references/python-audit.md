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

For a stronger assertion or conditional probe execution, read [probe execution](python-audit-advanced.md#stronger-probes). For several already-justified faults with one reusable baseline, read [batch mode](python-audit-advanced.md#several-already-justified-faults-one-baseline). Neither mode is needed just to assess one existing test against one fault.

For small, permitted package/test directories, select those directories plus required configuration rather than reconstructing their import dependencies file by file merely to minimize copy size. Directory selection preserves fixtures and support modules. Narrow the selection when size, scope, sensitive data or incompatible contents require it; do not copy a repository root, environment or unrelated data indiscriminately. The helper enforces its 20 MB input limit before execution.

Each check gets a fresh project-local disposable copy with verified imports and the copy as its working directory. Listed imports execute before the selected test runner.

The single-audit CLI emits JSON with `status` (`observed` or `incomplete`) and `checks`. Check keys are `correct_tests`, `mutant_tests` and, when run, `correct_probe`, `mutant_probe`. Each contains `exit_code`, `timed_out`, `output`, and `output_truncated`. Batch reuse references an earlier observation instead of duplicating its output, as described in batch mode. Inspect the actual failure in `output`; neither `observed` nor a nonzero mutant exit establishes coverage. `probe_skipped`, when present, explains unvalidated conditional probes; absent checks are not passes.

Correct-code failure or timeout stops as incomplete. CLI exit 0 means observations collected; exit 2 means invalid/incomplete evidence (invalid input may produce only stderr). Selected original bytes are checked and copies removed. Output retains a 12,000-character tail per check; invalid UTF-8 is replaced. Timeout defaults to 30 seconds per check; `--timeout` allows at most 300.

Limits: POSIX, Python 3.9+, 20 MB selected inputs; no symlinks/Git internals/path traversal or namespace-package import checks. No dependency installation. This is **not a sandbox**: use trusted tests, local data and authorized actions only. Files outside the selection are not integrity-checked or restored. Use normal project facilities for other languages or unsupported layouts; don't repeat a valid baseline merely to adopt this helper mid-audit.
