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

Each check gets a fresh project-local disposable copy with verified imports. Correct-code failure or timeout stops the audit. Selected original bytes are checked and generated copies removed. Exit 0 means observations collected, **not** adequate coverage: inspect failure reasons and each check's status. Exit 2 means invalid/incomplete evidence. Output is capped at 12,000 characters per check with truncation marked. Timeout defaults to 30 seconds per check; `--timeout` allows at most 300.

Limits: POSIX, Python 3.9+, 20 MB selected inputs; no symlinks/Git internals/path traversal or namespace-package import checks. No dependency installation. This is **not a sandbox**: use trusted tests, local data and authorized actions only. Files outside the selection are not integrity-checked or restored. Use normal project facilities for other languages or unsupported layouts; don't repeat a valid baseline merely to adopt this helper mid-audit.
