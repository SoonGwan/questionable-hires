I’ll check how request methods are converted, add a focused regression test, and run the relevant tests with the prepared Python environment. I’m using the receipt skill to verify that the test fails before the fix and passes afterward.

The regression reproduces the bug: byte methods return HTTP 405 from the local endpoint, while text methods pass. Requests already has a helper for converting bytes to native text; I’ll use it before the existing uppercase conversion.

Fixed sessions.py to decode byte methods using `to_native_string`, preserving uppercase normalization. Added regression coverage for byte and text methods.

Verification with Python 3.9.20 and local HTTP endpoints:

- `python -m pytest -q test_requests.py -k test_request_method_is_native_string`: before fix, 2 failed and 2 passed.
- Expanded pytest selection covering the regression, HTTP methods, redirects, preparation, and hooks: **26 passed**.
- `git diff --check`: passed.

Existing tests were unchanged. The full suite and Python 2.6/3.4 were not run; existing deprecation warnings remain.
