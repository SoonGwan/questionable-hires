# Python audit: bring the fault, not the plumbing

Run the CLI with the project's interpreter and actual installed skill path; pass
JSON on stdin, without a recipe file or wrapper. This interface is sufficient for
supported audits. Inspect source for a concrete trust, adaptation or troubleshooting
question. Adapt the files, binding and behavioral fault to the actual project:

Output is lossless compact JSON; `--pretty` adds indentation for manual reading.

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
Selected trees must contain only regular files/directories; symlinks and special
files (such as FIFOs or sockets) are rejected, not silently omitted from copies.
`imports` includes the affected implementation and must resolve inside each copy.
`old` matches `target` exactly once. `tests` supplies unittest or installed pytest
arguments. Optional `probe` runs the same stronger assertion on correct/faulty
code; omit when only checking existing protection.

Unknown fields are rejected. Set interpreter/deadline through CLI `--python` and
`--timeout`, not JSON keys. Each executed check uses a fresh project-local copy as
its working directory. Listed imports are verified before the precheck.

Unittest defaults to a Python bootstrap calling `unittest.main`. For required
`python -B -m unittest` execution, set `"invocation": "module"` and read the
[module-mode contract](python-audit-advanced.md#native-unittest-module-invocation).
This optional mode supports native test/probe files, not inline probes or pytest.

For native pytest checks, configuration and collection precede import verification
and the precheck, before test bodies. Selected test modules can therefore be listed
without bypassing native assertion rewriting. This does not run fixtures before
the precheck. Inline `probe` code uses direct import/precheck execution, not pytest
configuration or fixtures; use native probe files/replacements when those matter.

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
For fixture-based native probes or same-path test improvements read
[native files and replacements](python-audit-probes.md),
without loading unrelated advanced modes.
For several justified faults or required test-specific process exits, use
[batch mode](python-audit-batch.md)
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

For tasks that require whole-project preservation, optional `"guard_project": true`
adds `integrity.project_guard` after a successful before/after inventory check.
Authorize reading the entire source root first. It covers bytes/modes, added or
removed paths, directories, symlink identities and in-root Git metadata, not
external link targets or effects. It hashes rather than copies unselected files;
the `files` selection still determines execution-copy contents. Limits: 10,000
entries and 20 MB per inventory. Special files, raced file replacements and
over-budget trees fail explicitly. Default off: no unselected-tree reads or guard
claim. Changes are reported without restoration, including on incomplete checks;
inventory failure is not successful preservation. Stable trusted projects only,
not race isolation or a sandbox. In batch mode the flag is a shared recipe field.

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

Empty/skipped unittest suites or pytest no-tests (exit 5), precheck failure (6), import setup failure
or early exit (7) are incomplete. Broken runner helpers can cause false passes.
Pytest help/version without a verification session is incomplete too, not a baseline.
Do not change warning policy to credit detection. Read [diagnostics](python-audit-advanced.md#diagnostics-and-incomplete-evidence)
for these errors or cleanup trouble. Do not retry an unconfirmed child exit.

Limits: POSIX, Python 3.9+, 20 MB inputs; no symlinks/Git internals/traversal or
namespace-package import checks. No installation. Required work must finish in the
foreground; surviving background jobs and escaped groups are unsupported. This is
**not a sandbox**: trusted tests, local data and authorized actions only. Use project
facilities for unsupported layouts/languages; don't repeat a valid baseline to adopt
this helper mid-audit.

Selected-input copying and final byte/mode comparison validate the opened regular
file's identity and mode with nonblocking/no-follow opens. A replacement pipe,
symlink or different file between inspection and open is rejected instead of
waiting or accepting replacement bytes. Reads remain bounded if the same file
grows. This is not a concurrent snapshot: parent-directory races and edits to the
same open file are not isolated, and unchanged bytes/modes do not prove unchanged
identity throughout execution. Input collection has no whole-operation deadline.
