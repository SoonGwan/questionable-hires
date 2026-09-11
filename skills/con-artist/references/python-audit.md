# Python audit without rewriting isolation plumbing

Use `scripts/audit.py` for a small Python unittest/pytest audit with one exact text mutation. The helper uses only the standard library; pytest must already exist in the chosen interpreter. For another language, an existing project mutation tool, non-text mutations, or inputs above 20 MB, keep the normal isolated workflow. Do not install a framework to use this helper.

Write a short JSON recipe locally. Paths below are illustrative; choose the actual task files, import names and fault. Never copy the example fault blindly.

```json
{
  "files": ["service.py", "test_service.py"],
  "imports": ["service"],
  "target": "service.py",
  "old": "    store.append(record)\n",
  "new": "",
  "runner": "unittest",
  "tests": ["-v", "test_service"],
  "probe": "from service import save\ns = ['existing']\nsave(s, 'record')\nassert s == ['existing', 'record']\n"
}
```

From the project directory, use the skill's actual installed path:

```sh
python3 /path/to/con-artist/scripts/audit.py --spec audit-recipe.json --python /path/to/project/python
```

- `files`: explicit project-relative files/directories needed for imports, tests and configuration. Symlinks, parent traversal and Git internals are rejected. Include package/configuration files the test runner actually needs; no automatic repository sweep occurs.
- `imports`: production module names that must resolve inside each disposable copy. Include the affected implementation. Namespace packages without `__file__` are unsupported. This check is not a proof that every dependency or runtime path stays local.
- `old` must occur exactly once in the selected `target`; identical replacements are rejected. Tests/configuration are otherwise copied unchanged.
- `runner`: `unittest` (default) or existing `pytest`; `tests` are its argument list. Do not pass flags that authorize external side effects or unsafe writes.
- `probe`: optional Python assertion code; use it for the stronger behavioral check, not a replacement implementation. The same code runs on correct and faulty versions. Omit it when only checking an existing assertion. Do not rerun an already valid baseline just to adopt this helper mid-audit.

Each check starts in a fresh disposable copy inside the source project. Imports are checked in the same interpreter process as the test/probe. Correct-code failure stops the audit; timeouts stop the audit and terminate its process group. Output contains separate exit codes, timeout flags and the last 12,000 output characters per check, with truncation marked. Nonzero mutant exit is **not** automatically scored as a killed fault: inspect whether the intended assertion failed rather than import/configuration errors.

Exit 0 means observations were collected, not that coverage is adequate. Exit 2 means invalid/incomplete evidence. The helper checks selected original file bytes after execution and never restores or overwrites user files. It removes only its generated temporary copies. It is **not a security sandbox**: tests remain arbitrary trusted project code and may access external paths/services. Preserve the user's authorization boundary, use local data, and don't use it on untrusted tests. Original files outside `files` are not integrity-checked. The current process cleanup requires POSIX and Python 3.9+.
