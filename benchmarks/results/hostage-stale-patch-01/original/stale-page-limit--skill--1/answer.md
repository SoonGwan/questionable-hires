I’ll use the hostage-negotiator skill to keep this focused. I’ll read the project requirements, attempt the patch unchanged, and adapt it if needed before running the native tests.

The unchanged patch was rejected with exit 1: `options.py:1` did not match. The current code uses `or 100`, which turns zero into 100. I’ll replace it with an explicit `None` check.

Fixed `options.py`: missing/`None` defaults to 100; zero and positive integers remain unchanged, preserving inputs.

- Original `git apply requested.patch` failed with exit **1**: `options.py:1` did not apply. Adapted fix applied successfully.
- Native unittest run: **4 tests passed**, process exit **0**.
- `git diff --check`: exit **0**.

Preserved the patch, existing tests, other original files, and HEAD. Only `options.py` was edited; the runner appended its audit entry.
