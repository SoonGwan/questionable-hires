Search QA
=========

Confirmed failure: type `ca`, then `cat` before the first request finishes.
When `cat` finishes first, its result is displayed correctly. When the older
`ca` request finishes afterward, Search overwrites the display with `ca`.
`search.py` assigns each response without checking whether its query is latest.

Rerun from this directory (Python standard library only):

```sh
python3 -B -m unittest -v test_search_overlap
```

Observed results against actual `search.Search`:

- Normal overlapping completion (`ca` then `cat`): PASS. After both requests
  finish, the display contains `results for cat`. No intermediate display
  value is required while `cat` remains pending.
- Reversed completion (`cat` then `ca`): FAIL. The assertion that completed
  `cat` is initially displayed passes. After both requests finish, the final
  assertion observes `results for ca` instead of `results for cat`.

The full unittest output, including the actual failing assertion and traceback,
is saved in `search_qa_output.txt`. Exit code is 1 because the regression test
intentionally requires the documented behavior; the failure is not marked as
expected or swallowed.

Controls in `test_search_overlap.py` assert query submission order, that both
actual Search.run tasks overlap with unreleased response futures, that releasing
one response finishes only its request, and the exact completion order. Events
and futures control scheduling without sleeps or network access. All waits have
a two-second bound. A finally block cancels and drains owned tasks and cancels
unreleased futures on success, assertion failure, or timeout.

Production files were preserved. This QA adds only the test, this report, and
the captured output. It exercises the asynchronous Search model supplied by
this project; the project contains no browser UI.
