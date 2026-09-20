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
cleanup, not arbitrary effects or unselected files. After verifying the proposed
tests, apply only the authorized test edit and retain unchanged tested bytes.

Boundaries: trusted local tests, Python 3.9+/POSIX, no sandbox; no symlink inputs,
Git internals or parent paths. Shared input budget 20 MB; 30 seconds/check by
default (`--timeout`, maximum 300), last 12,000 output characters per check.
Remaining foreground process-group members are stopped; persistent background
work is unsupported. A cleanup failure is not permission to retry live work.

Only when needed: [common options](python-audit.md) covers conditional probes,
output and interpreter flags; [other native probes](python-audit-probes.md)
covers new files; [advanced details](python-audit-advanced.md) covers import roots,
binding prechecks and incomplete-evidence diagnostics. This recipe needs none of
those references for the ordinary four-check workflow.
