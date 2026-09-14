I’ll use the mother-in-law skill to add the three controlled async regression cases, then run the four-test native suite once and retain any product failures.

The existing fixture provides controlled responses and bounded task cleanup. `Pager.select` clears `loading` whenever any request finishes, so I expect both overlap tests to expose that fault. I’ll assert the full state after the older request completes, while the newer request is still pending, and also check latest completion and error/retry recovery.

Added exactly three tests in `test_pager.py`; preserved the existing test and all other files.

Ran once at the native Python async unit-test layer. Results under `test_pager.PagerTests`:

- `test_single_success`: PASS
- `test_older_success_while_newer_pending`: FAIL
- `test_older_oserror_while_newer_pending`: FAIL
- `test_latest_error_followed_by_successful_retry`: PASS

Both failures demonstrate premature `loading=False` after older completion while the newer request remains pending. Expected state: `(['cached'], True, None)`; observed: `(['cached'], False, None)`. Latest-success assertions passed. Regression failures remain; production is unchanged.

Complete command, bounded to 15 seconds:

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_pager"], timeout=15).returncode)'
```
