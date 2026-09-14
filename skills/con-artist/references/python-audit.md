# Python audit: bring the fault, not the plumbing

Run the CLI with the project's interpreter and actual installed skill path; pass
JSON on stdin, without a recipe file or wrapper. This interface is sufficient for
supported audits. Inspect source for a concrete trust, adaptation or troubleshooting
question. Adapt the files, binding and behavioral fault to the actual project:

Use complete module/package copies when extraction would lose future flags,
closures or decorators. A shorter extracted function is not an equivalent runtime.

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
  "probe_when": "survives",
  "precheck": "import service, test_service\nassert test_service.SaveTests.test_acknowledges_save.__globals__['save'] is service.save\nprint('Verified actual test global save is service.save', flush=True)\n",
  "probe": "from service import save\ns = ['existing']\nsave(s, 'record')\nassert s == ['existing', 'record']\n"
}
JSON
```

`files` selects relative files/directories and needed configuration. Select small
permitted packages/test directories together to preserve fixtures and imports;
narrow for size, scope or sensitive data, not to reconstruct every dependency.
`imports` includes the affected implementation and must resolve inside each copy.
`old` matches `target` exactly once. `tests` supplies unittest or installed pytest
arguments. Optional `probe` runs the same stronger assertion on correct/faulty
code; omit when only checking existing protection.

Unknown fields are rejected. Set interpreter/deadline through CLI `--python` and
`--timeout`, not JSON keys. Each executed check uses a fresh project-local copy as
its working directory, with listed imports before the precheck and native runner.

For pytest, list implementation modules in `imports`, not selected test modules:
pre-importing tests bypasses pytest's assertion rewriting and can lose useful
expected/observed diagnostics. Let pytest collect its tests normally.

`precheck` is optional: the unittest example illustrates checking an imported
function binding. It does not require an equivalent pytest plugin. Use existing
copied-import evidence and the traced behavioral path when they resolve the claim.
Add same-process checks for required or unresolved bindings; a precheck cannot
establish later fixture rebinding. Use a native hook only when that later binding
matters. Import/setup or precheck failures are incomplete, never killed faults.

The example validates a stronger assertion only if tests miss the fault, using
`"probe_when": "survives"`. Omit that field (or use `"always"`) when the request
requires validating the stronger assertion regardless. A nonzero mutant
exit skips conditional probes; inspect the failure before calling it detection.
For fixture-based native probes read [probe_files/probe_tests](python-audit-probes.md),
without loading unrelated advanced modes.
For several justified faults or required test-specific process exits, use
[batch mode](python-audit-advanced.md#several-already-justified-faults-one-baseline)
to share recipe setup; different test selections still execute their own baselines.

For an evidenced `src/` or other explicit project import path, see
[copied import roots](python-audit-advanced.md#copied-import-roots). Do not install
the project or guess import paths merely to make a check green.

Read the returned evidence rather than rerunning completed checks:

- `Copied process:` and `Verified copied import:` report interpreter/copy path
  and module path/SHA-256 in each child. Reuse these instead of duplicating hashes.
  They do not prove function execution, code-object identity or later bindings.
- `integrity` reports `selected_files`, `selected_original_bytes_and_modes_unchanged`
  and `owned_scratch_removed` after checking them. This does not cover unselected
  files, new original-tree files, later commands or coverage. Changes/removal
  failures raise errors; originals are not silently restored.

Single-audit JSON has `status` (`observed`/`incomplete`) and `checks`: `correct_tests`,
`mutant_tests`, and executed `correct_probe`/`mutant_probe`. Each check has
`exit_code`, `timed_out`, `output`, `output_truncated`. Inspect native counts and
actual assertions/warnings, not just exit/status. `probe_skipped` means unvalidated
conditional probes; missing checks/output are not passes. Batch reuse points to
an earlier observation, not another execution.

Correct-code failure/timeout stops as incomplete. CLI 0 means observations collected,
not protection proved; CLI 2 means invalid/incomplete (possibly stderr only).
Each check retains a 12,000-character output tail, replacing invalid UTF-8;
provenance can also be truncated. Timeout defaults to 30 seconds/check, max 300.

Empty/skipped unittest suites (exit 5), precheck failure (6), import setup failure
or early exit (7) are incomplete. Broken runner helpers can cause false passes;
do not change warning policy to credit detection. Read [diagnostics](python-audit-advanced.md#diagnostics-and-incomplete-evidence)
for these errors or cleanup trouble. Do not retry an unconfirmed child exit.

Limits: POSIX, Python 3.9+, 20 MB inputs; no symlinks/Git internals/traversal or
namespace-package import checks. No installation. Required work must finish in the
foreground; surviving background jobs and escaped groups are unsupported. This is
**not a sandbox**: trusted tests, local data and authorized actions only. Use project
facilities for unsupported layouts/languages; don't repeat a valid baseline to adopt
this helper mid-audit.
