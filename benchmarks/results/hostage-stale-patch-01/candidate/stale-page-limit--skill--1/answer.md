I’m using the hostage-negotiator skill to keep this fix focused. I’ll read the project requirements, attempt the supplied patch unchanged, and capture its result before adapting it if needed.

`git apply requested.patch` exited with code 1: the patch does not apply to the current `options.py`. Its current fallback treats zero as missing. I’ll adapt the fix to default only when the value is `None`, then run the native suite.

Fixed `options.py`: missing/`None` defaults to 100; zero and positive integers are preserved without modifying input.

- Original patch attempt exited **1**: `patch failed: options.py:1`; `patch does not apply`.
- Adapted edit successfully applied.
- `python3 -B -m unittest discover -v`: **4 tests, all passed; test-process exit 0**.
- Diff check passed. Only `options.py` was edited; tests, supplied patch, other original files, and HEAD were preserved. The runner-created invocation log was left untouched.
