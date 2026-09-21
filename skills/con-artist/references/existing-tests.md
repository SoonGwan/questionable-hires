# Improve an existing native test

Use adequate project comparison support if it already exists. Otherwise this
optional CLI compares original/proposed tests against correct/faulty code in four
fresh project-local copies. It preserves native paths, fixtures and test-file modes;
it never applies the proposed edit or deliberate fault to the source project.

Adapt this complete recipe to the actual files, reachable fault and stronger test.
Use the project's interpreter and installed skill path. No wrapper or saved recipe
is required; `probe_replacements` contains the complete proposed test file.

```sh
/path/to/project/python /path/to/con-artist/scripts/audit.py --source . --spec - <<'JSON'
{
  "files": ["service.py", "test_service.py"],
  "imports": ["service"],
  "target": "service.py",
  "old": "    values.append(value)\n",
  "new": "",
  "runner": "unittest",
  "tests": ["-v", "test_service"],
  "probe_replacements": {
    "test_service.py": "import unittest\nfrom service import save\nclass Tests(unittest.TestCase):\n    def test_saved(self):\n        values = []\n        self.assertTrue(save(values, 'item'))\n        self.assertEqual(values, ['item'])\n"
  },
  "probe_tests": ["-v", "test_service"]
}
JSON
```

Select existing relative files/directories needed by the native tests, including
configuration and fixtures. `old` must match `target` exactly once. Replacement
paths must be selected existing test/support files, not the mutation target.
Keep required tests and fixture behavior; do not change production to fit the tool.
For installed pytest, use `runner: "pytest"` and its native test arguments in both
test lists. Configuration/collection precede copy-import verification; fixtures run
normally afterward. No automatic package installation or custom plugin is required.

For exact `python -B -m unittest` checks, add `"invocation": "module"` and read
the [instrumentation and startup limits](python-audit-advanced.md#native-unittest-module-invocation).
The default uses `unittest.main` in a bootstrap, not module invocation.

If the task also requires preserving unselected files, new paths and Git metadata,
and reading the whole project is permitted, add `"guard_project": true` to the
recipe. It inventories the source root before execution and after scratch cleanup;
no separate hash wrapper is needed. This optional guard is bounded to 10,000
entries and 20 MB per inventory. It records symlinks without reading their targets;
external Git/worktree metadata is outside its scope. Changes raise without being
restored. It is not a sandbox, atomic snapshot or protection from concurrent edits.

When the audit requires the test's imported function binding in the same process,
the helper already supports this without writing your own startup hook.
For the example above, include `test_service` in `imports` and add:

```json
"precheck": "import service, test_service\nassert test_service.save is service.save\nprint('Verified test binding: test_service.save is service.save', flush=True)\n"
```

Adapt the actual consumer alias, not just the implementation module name. This
checks the loaded binding before native tests/probes, not later fixture rebinding
or call counts. Existing runtime observations may already be sufficient; do not
add a precheck or tracer merely to repeat them. A failed precheck is incomplete
evidence, not a detected behavioral fault. For a discovered test module outside
the copy root, use the project's evidenced [import roots](python-audit-advanced.md#copied-import-roots)
so the verified module is the one the native runner actually uses.

Read all four named `checks`: `correct_tests`, `mutant_tests`, `correct_probe`,
`mutant_probe`. Each retains native output/exit, timeout and truncation. A passing
correct check and a defect-specific faulty assertion establish sensitivity;
syntax/setup failures, empty/skipped tests or a bare nonzero exit do not. The
`Verified copied import:` lines identify loaded copy files and hashes, not later
fixture rebinding or proof that a function was called. Instrument only an unresolved
or requested binding/effect. Use native observations rather than rerunning for logs.

`status: "incomplete"` or CLI 2 means the comparison was not established; missing
checks are unrun. CLI 0 means observations collected, not that the mutation was
detected. `integrity` confirms selected original bytes/modes and owned-scratch
cleanup. With the optional guard, `integrity.project_guard` additionally reports
whole-root preservation; without it, unselected files are not covered. Neither
mode proves arbitrary external effects absent. After verifying the proposed
tests, apply only the authorized test edit and retain unchanged tested bytes.

Boundaries: trusted local tests, Python 3.9+/POSIX, no sandbox; selected inputs
must be regular files/directories (no FIFO/socket/device or symlink inputs),
Git internals or parent paths. Shared input budget 20 MB; 30 seconds/check by
default (`--timeout`, maximum 300), last 12,000 output characters per check.
Remaining foreground process-group members are stopped; persistent background
work is unsupported. A cleanup failure is not permission to retry live work.

Only when needed: [common options](python-audit.md) covers conditional probes,
output and interpreter flags; [other native probes](python-audit-probes.md)
covers new files; [advanced details](python-audit-advanced.md) covers import roots,
binding prechecks and incomplete-evidence diagnostics. This recipe needs none of
those references for the ordinary four-check workflow.
