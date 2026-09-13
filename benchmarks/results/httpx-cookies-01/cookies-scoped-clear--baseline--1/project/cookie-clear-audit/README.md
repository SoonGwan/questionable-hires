Cookie clearing coverage audit

Existing coverage detects dropping the path argument from Cookies.clear: the
faulty copy clears the entire requested domain. No other behavior was mutated.
See mutation.diff and faulty_suite.log.

Correct copy: tests/models/test_cookies.py — 7 passed.
Faulty copy: 6 passed, 1 failed. The detecting assertion is
`assert len(cookies) == 1` at tests/models/test_cookies.py:50 in
`test_cookies_with_domain_and_path`; actual length is zero.
The subsequent delete of /subpath/2 and empty-jar assertion also establish
which same-domain path survives on correct code.

The scoped test has no other-domain cookie. Cross-domain preservation during
scoped clearing is therefore not directly asserted by this file. The selected
mutation demonstrates sensitivity to same-domain over-deletion, not exhaustive
coverage of every possible scope violation. No additional scoped regression
test is needed to detect this already-detected fault.

Domain-only control on both correct and faulty copies:
- Existing test_cookies_with_domain passes independently.
- domain_control.py seeds two paths in example.com and one in example.org,
  clears example.com without a path, and asserts the exact remaining cookie is
  the example.org cookie. Both pass. Each process verifies its local import.

All Python/pytest invocations used
<ENV>/venv/bin/python.
No dependencies were installed. Pytest plugin autoload and cache provider were
disabled; bytecode writes were disabled. Original source/tests were not edited;
SHA-256 verification of all original files passed (integrity.txt).
Disposable source/test copies and logs are contained in this directory.
