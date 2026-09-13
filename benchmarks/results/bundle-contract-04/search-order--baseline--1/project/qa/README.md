# Search overlap reproduction

Run from the project root with the existing Python standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s qa -v
```

Current result: two tests run, normal completion passes, reversed completion
fails the latest-query assertion (exit status 1). The failing test is intentionally
left as a regression test, not marked as an expected failure.
`search-overlap-results.txt` contains the captured run, including control states
and the actual assertion traceback.

The tests import the production `Search` from `search.py`. A controlled fetch
double uses separate response futures for successive queries `ca` and `cat`.
Events establish that both requests have entered fetch before either is released.
Assertions verify query invocation order, both requests pending, no initial
result, and the first displayed response while the other request remains pending.
The test then releases and awaits the remaining request and asserts that the
latest query's result is displayed.

| Completion order | Required final display | Actual final display | Outcome |
| --- | --- | --- | --- |
| `ca`, then `cat` | `results for cat` | `results for cat` | Pass |
| `cat`, then `ca` | `results for cat` | `results for ca` | Fail |

This reproduces a realistic typing interaction: an earlier search takes longer
than a later search. `Search.run` unconditionally assigns every completed response
to `result`, allowing stale results to overwrite the latest results.

Scheduling uses explicit gates, not sleeps or network timing. Each
behavior-dependent wait has a one-second timeout. A `finally` block cancels
unfinished owned tasks, drains all owned tasks with a bounded gather, and cancels
unused response futures. No dependencies or external services are used.

Production files were preserved. SHA-256 values before and after testing:

```text
b0a6a31914493956af57224dfbf16f1e8f128693717595e6723610b588fc02ea  search.py
369fc267423af64f55359324c33516352e40bdc7ed6467df7f8596e48bab620f  requirements.md
```
