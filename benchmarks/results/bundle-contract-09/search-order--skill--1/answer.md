I’ll use the mother-in-law skill to test overlapping requests against the actual Search implementation, preserve production files, and leave a rerunnable local regression test.

Search assigns every completed response directly to the displayed result, so an older request appears able to overwrite a newer result. I’ll test both completion orders with controlled responses, asserting only the final result for normal order and checking that the latest result survives the older response in reversed order.

Reproduced a stale-response bug against actual `Search` at the component layer:

- **Normal order passed:** `ca` then `cat` complete; final result is `latest: cat`. Intermediate display is observation only.
- **Reversed order failed:** `cat` completes first and displays correctly; completing `ca` overwrites it. Actual assertion: `'older: ca' != 'latest: cat'`.

Saved rerunnable tests in `test_search.py` with standalone `controlled_fetch.py`. Waits are bounded; owned tasks are cancelled and drained. Production files and existing user changes are preserved.

Run with a 15-second overall bound:

```sh
python3 -B -c 'import subprocess, sys; sys.exit(subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", "test_search"], timeout=15).returncode)'
```

Result: **2 tests, 1 failure**, with controls and assertions printed.
