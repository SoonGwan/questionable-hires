I’ll run the exact tests before editing, capture the assertion failure, then make the fix in `httpx/_urls.py`, rerun the same command, and review the focused diff.

The pre-edit run produced `1 failed, 2 passed`: setting `a` to `456` returned `?a=123&a=456` instead of `?a=456`. `copy_set_param` calls `QueryParams.add`; I’ll switch that call to the existing `QueryParams.set` method.

Fixed `URL.copy_set_param` in `httpx/_urls.py:343` by changing `self.params.add(...)` to `self.params.set(...)`.

- Before: **1 failed, 2 passed**. The assertion expected `?a=456` but received `?a=123&a=456`.
- After, using the exact same command: **3 passed**.
- Reviewed the one-line diff; `git diff --check` passed.

Only `httpx/_urls.py` changed. The public API, neighboring add/remove methods, tests, and all other files were preserved.
