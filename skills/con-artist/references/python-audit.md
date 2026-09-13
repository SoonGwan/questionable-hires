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
  "precheck": "import service, test_service\nassert test_service.SaveTests.test_acknowledges_save.__globals__['save'] is service.save\nprint('Verified actual test global save is service.save', flush=True)\n",
  "probe": "from service import save\ns = ['existing']\nsave(s, 'record')\nassert s == ['existing', 'record']\n"
}
JSON
```

`files` selects relative files/directories including needed configuration. `imports` must include the affected implementation and resolve inside each copy. `old` must match `target` exactly once. `tests` supplies arguments for unittest or already-installed pytest. Optional `probe` is the same stronger assertion code for correct/faulty versions, not a replacement implementation. Omit it when only checking existing protection.

Unknown recipe fields are rejected before execution rather than ignored; for
example, `probes` is not `probe`. Set execution options using CLI `--timeout`
and `--python`, not JSON keys. The optional mode fields are described below.

For pytest, list implementation modules in `imports`, not selected test modules:
pre-importing tests bypasses pytest's assertion rewriting and can lose useful
expected/observed diagnostics. Let pytest collect its tests normally.

Optional `precheck` runs after copied imports, before each check in that same
process. Use it for required caller-binding checks, not a separate binding module.
It establishes current bindings, not later calls or immunity to fixture rebinding;
use native hooks for post-collection checks without pre-importing pytest tests.
Precheck failure (check exit 6) is incomplete evidence, never a killed fault.
Listed-import setup failure or early exit uses reserved check exit 7 and stops
as incomplete even on a mutant; see [diagnostics](python-audit-advanced.md#diagnostics-and-incomplete-evidence).

For native fixture-based assertions, use `probe_files`/`probe_tests` from
[probe execution](python-audit-advanced.md#stronger-probes), avoiding nested Python
strings; that section also covers conditional execution. For several already-justified
faults with one reusable baseline, read [batch mode](python-audit-advanced.md#several-already-justified-faults-one-baseline).
Neither mode is needed just to assess one existing test against one fault.

For an evidenced `src/` or other explicit project import path, see
[copied import roots](python-audit-advanced.md#copied-import-roots). Do not install
the project or guess import paths merely to make a check green.

For small, permitted package/test directories, select those directories plus required configuration rather than reconstructing their import dependencies file by file merely to minimize copy size. Directory selection preserves fixtures and support modules. Narrow the selection when size, scope, sensitive data or incompatible contents require it; do not copy a repository root, environment or unrelated data indiscriminately. The helper enforces its 20 MB input limit before execution.

Each executed check gets a fresh project-local disposable copy with verified imports and the copy as its working directory. Batch mode can reuse successful correct-code observations as documented above. Listed imports execute before the selected test runner.

Each check prints `Copied process:` (interpreter and absolute copy directory)
and `Verified copied import:` (module, relative file path and SHA-256) in that
same process. Reuse this provenance instead of writing another file-hashing
precheck. These are imported-file observations, not proof of function execution,
code-object identity or later fixture bindings; use `precheck`/native hooks when
those are required. Provenance shares the output tail limit and can be truncated.

The single-audit CLI emits JSON with `status` (`observed` or `incomplete`) and `checks`. Check keys are `correct_tests`, `mutant_tests` and, when run, `correct_probe`, `mutant_probe`. Each contains `exit_code`, `timed_out`, `output`, and `output_truncated`. Batch reuse references an earlier observation instead of duplicating its output, as described in batch mode. Inspect the actual failure in `output`; neither `observed` nor a nonzero mutant exit establishes coverage. `probe_skipped`, when present, explains unvalidated conditional probes; absent checks are not passes.

Correct-code failure or timeout stops as incomplete. CLI exit 0 means observations collected; exit 2 means invalid/incomplete evidence (invalid input may produce only stderr). Output retains a 12,000-character tail per check; invalid UTF-8 is replaced. Timeout defaults to 30 seconds per check; `--timeout` allows at most 300.

`integrity` reports `selected_files`,
`selected_original_bytes_and_modes_unchanged` and `owned_scratch_removed` only
after those checks finish. Reuse this result instead of writing a second hash/
cleanup check for the same selected inputs. It can accompany incomplete test
evidence; it does not establish coverage, protect unselected files, inventory
new original-tree files or cover later commands. Detected original changes or
unconfirmed removal raise an error, never a successful integrity result; original
changes are not silently restored.

Empty/skipped unittest suites give check exit 5, not a valid baseline. Inspect
actual assertion failures and warnings: broken runner helpers can cause errors or
false passes. Do not change warning policy to credit a kill. For empty suites,
precheck errors, assertion plumbing or cleanup failures, read
[diagnostics](python-audit-advanced.md#diagnostics-and-incomplete-evidence).
An unconfirmed child exit stops the audit; do not retry while it may remain.

Limits: POSIX, Python 3.9+, 20 MB selected inputs; no symlinks/Git internals/path traversal or namespace-package import checks. No dependency installation. This is **not a sandbox**: use trusted tests, local data and authorized actions only. Files outside the selection are not integrity-checked or restored. Use normal project facilities for other languages or unsupported layouts; don't repeat a valid baseline merely to adopt this helper mid-audit.
