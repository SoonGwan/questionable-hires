# Search overlap QA

Run from this project with the standard library only:

```sh
python3 -B -m unittest -v test_search_overlap.py
```

The test imports the actual `Search` from `search.py`. Each fetch waits on its
own future; events confirm that the older `ca` request has started before the
newer `cat` request starts. Assertions verify both requests are pending before
either response is released, and that the unreleased request stays pending.
Completion order is explicitly controlled without sleeps. Each behavior-dependent
wait has a two-second timeout. A `finally` block cancels pending gates and tasks
and gathers all owned tasks with a timeout, including on assertion failure.

Observed run:

```text
test_normal_completion_keeps_latest_final_result ... ok
test_reversed_completion_does_not_overwrite_latest ... FAIL
AssertionError: 'results for ca' != 'results for cat'
 : latest query must remain visible after both finish (('cat', 'ca'))
Ran 2 tests in 0.012s
FAILED (failures=1)
```

Normal completion releases `ca`, waits for it to finish, then releases `cat`.
The assertion that the final display is `results for cat` passes. There is no
assertion about the intermediate display while `cat` is pending.

Reversed completion releases `cat` first. The assertion that the display is
`results for cat` passes while `ca` remains pending. Releasing `ca` then changes
the display to `results for ca`, failing the final latest-result assertion.
This reproduces a realistic stale-response race when a user types another
character and the newer request completes faster than the older request.
`Search.run` unconditionally assigns the response on completion, with no check
that the request still represents the latest query.

The regression test intentionally fails until that production behavior is fixed.
Production files were not edited.
