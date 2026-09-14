I’m using the mother-in-law skill to add the three native regression cases, then run the four-test suite once and retain any product failures.

The three tests now check request keys and rows/loading/error at each required transition. The overlap checks use subtests so a stale-completion failure still allows verification of the newer request’s final state. I’ll run the suite with the fixture’s one-second wait limits and a 20-second overall timeout.

Changed only `test_pager.py`, preserving the existing test. Ran once: **4 tests, 2 passed, 2 failed**.

Native identities under `test_pager.PagerTests`:

- `test_single_success` — PASS
- `test_older_success_while_newer_pending` — FAIL
- `test_older_oserror_while_newer_pending` — FAIL
- `test_latest_error_then_successful_retry` — PASS

Both failures demonstrate that older completion clears `loading` while the newer request remains pending. Expected `(['cached'], True, None)`; observed `(['cached'], False, None)`. Newer success and error/retry transitions passed.

Tested layer: native async `Pager.select` with controlled responses, bounded waits, and fixture-owned cleanup. Production unchanged; regression failures retained.

Complete bounded command:

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_pager"], timeout=20).returncode)'
```
