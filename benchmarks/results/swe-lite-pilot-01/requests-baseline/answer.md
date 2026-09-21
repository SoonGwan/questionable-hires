I’ll inspect method handling and the existing tests, add a focused fix, and verify it with the prepared Python environment.

Requests already has a helper that decodes byte strings to the native string type. I’ll use it for the session method and add a regression test covering uppercase and lowercase byte methods for GET and POST.

Fixed sessions.py to decode byte methods with `to_native_string()` before uppercasing. Added regression coverage for uppercase/lowercase byte GET and POST methods.

Verification using Python 3.9.20 and local HTTPBIN:
- Regression failed before the fix with HTTP 405.
- `python -m pytest -q test_requests.py -k 'method_name or HTTP_ or TestRedirects or test_basic_building or test_no_content_length'` — **14 passed**.
- `git diff --check` — passed.

Existing deprecation warnings remain. Full-suite and Python 2.6/3.4 verification were not performed.
