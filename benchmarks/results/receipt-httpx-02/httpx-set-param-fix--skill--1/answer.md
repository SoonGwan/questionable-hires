I’ll use the receipt skill to capture the native test failure, fix only `httpx/_urls.py`, and rerun the unchanged command before reviewing the focused diff.



The tests reproduced the defect: setting `a` returned `?a=123&a=456` instead of `?a=456`; add and remove both passed. I’ll change `copy_set_param` to call the existing `QueryParams.set` method.



Fixed `URL.copy_set_param` in `httpx/_urls.py:343` by replacing `self.params.add(...)` with `self.params.set(...)`.

Ran your exact command unchanged before and after:

- Before: **1 failed, 2 passed**. The set assertion expected `?a=456` but received `?a=123&a=456`.
- After: **3 passed**. Neighboring add/remove behavior remains covered.

Reviewed the one-line diff; `git diff --check` passed. No other files, including tests and existing untracked `.agents/` files, were changed.

Base revision: `8ed44f4f3d3c06bc408b378e435f9e106a7d4254`. Verification was limited to the three requested tests.
