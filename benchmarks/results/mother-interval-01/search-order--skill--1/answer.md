I’ll use the mother-in-law skill to test normal and reversed request completion against the actual Search, keeping production files unchanged.


The project has a minimal `Search` class and no existing test runner. Its implementation appears vulnerable to a stale response overwriting the latest result. I’ll add standard-library tests with controlled request completion, plus an isolated assertion-failure control. The normal-order test will leave the intermediate display unspecified, as required.


Reproduced a stale-response failure against actual `Search` at the component layer:

- **Normal order:** `c` then `cat`; both finish, latest result remains. Pass.
- **Reversed order:** `cat` finishes first, then `c` overwrites it. Assertion: expected `'CAT_RESULT'`, observed `'C_RESULT'`.
- Deliberate assertion-failure control passed. Intermediate display is not constrained.

Kept rerunnable tests in `test_search.py` and `search_test_support.py`. Waits and task cleanup are bounded. Production files and existing user changes are preserved.

Run from the project directory (15-second overall limit; currently reports one regression failure):

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_search"], timeout=15).returncode)'
```
