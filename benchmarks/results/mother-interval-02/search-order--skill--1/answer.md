I’ll use the mother-in-law skill to test overlapping requests against the actual Search implementation, keep a rerunnable local regression test, and leave production files unchanged.

Search assigns every completed response directly to the displayed result, so an older request appears able to overwrite a newer result. There’s no existing test suite. I’ll add standard-library tests for both completion orders, with no display assertion while the newer request is pending.

Reproduced a stale-response bug against actual `Search` at the component layer:

- **Normal order:** both requests overlap; older finishes first. After both finish, latest result is visible. **PASS**
- **Reversed order:** latest finishes first and displays correctly; older then overwrites it. Expected `'latest result'`, observed `'older result'`. **FAIL**

Saved rerunnable tests in `tests/test_search.py` with local controlled transport. Intermediate display during normal completion is unconstrained. All waits are bounded; owned tasks are cancelled and drained. Production files and existing user changes remain untouched.

Rerun with a 15-second overall bound:

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], timeout=15).returncode)'
```

Current result: **2 tests, 1 assertion failure**.
