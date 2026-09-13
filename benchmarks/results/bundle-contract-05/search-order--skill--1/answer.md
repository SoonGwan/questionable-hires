I’ll use the mother-in-law skill to test actual Search with controlled overlapping requests, keep a rerunnable regression test, and leave production files unchanged.

Search assigns every completed response to the displayed result, so a slower earlier request appears able to overwrite a newer result. I’ll test both completion orders and check the controlled transport’s assertion failure path. The normal-order test will leave the pending display unconstrained, as required.

Reproduced a stale-response bug against actual `Search` at the Python component layer.

- **Normal order:** start `c`, then `cat`; finish `c`, then `cat`. Final latest-result assertion passes. Pending display is unconstrained.
- **Reversed order:** finish `cat`, verify its result, then finish `c`. Assertion fails: expected `'latest result'`, observed `'older result'`.
- Deliberate transport mismatch correctly raises `AssertionError`.

Kept rerunnable `test_search.py` and `controlled_fetch.py`. Waits and task cleanup are bounded; owned tasks are cancelled and awaited. Production files and existing user changes are preserved.

Run from the project directory (15-second overall bound; currently 2 pass, 1 fails):

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "test_search.py"], timeout=15).returncode)'
```
