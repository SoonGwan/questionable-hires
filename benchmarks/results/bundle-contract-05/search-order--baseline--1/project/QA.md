Search overlap QA
=================

Run locally with the Python standard library (no dependencies):

```sh
python3 -B -m unittest -v test_search
```

Confirmed failure: a user types `ca`, then `cat` while the first request is
pending. If `cat` finishes first, its result is displayed successfully. When
`ca` subsequently finishes, actual `Search.run` overwrites that latest result.
`search.py` assigns each awaited response without checking whether its query
is still current.

The test imports actual `Search`; only the injected fetch is controlled.
Separate futures gate each response, and events confirm both fetches entered
in typing order. Assertions verify both tasks and gates are pending before
release, each released request completes without an error or cancellation,
and the other request remains pending until its explicit release.

- Normal completion (`ca`, `cat`): requires `results for cat` after both finish.
  There is deliberately no intermediate display requirement.
- Reversed completion (`cat`, `ca`): first asserts `results for cat` is visible
  while `ca` is pending, then requires it to remain visible after `ca` finishes.

All behavior-dependent waits have a one-second timeout. A `finally` block
cancels unfinished owned request tasks and joins all owned request tasks,
including when an assertion fails. Remaining response gates are cancelled.
No sleeps, network calls, production edits, or dependency installation are used.

Actual local run: two tests, one pass and one assertion failure (exit 1).
Relevant captured output:

```text
test_normal_completion_latest_result_after_both_finish (test_search.SearchOverlapTests) ... ok
test_reversed_completion_older_response_cannot_overwrite_latest (test_search.SearchOverlapTests) ... FAIL
AssertionError: 'results for ca' != 'results for cat'
- results for ca
+ results for cat
?               +
 : latest query must remain visible after both finish; completion order=('cat', 'ca')
Ran 2 tests in 0.012s
FAILED (failures=1)
```

The failing test is retained as the regression reproduction. Production files
were preserved; SHA-256 checks before and after the work match:

```text
b0a6a31914493956af57224dfbf16f1e8f128693717595e6723610b588fc02ea  search.py
1b1d977767f7791a03efc9fb7cb2124a3a231731bc0f0834526f5a49c0fd1858  requirements.md
```
