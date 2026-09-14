I’ll use the mother-in-law skill to test normal and reversed overlapping requests against the actual Search, keeping production files unchanged and leaving a rerunnable local regression.


The contract requires the latest result after both requests finish, with no required display while the newer request is pending. Search currently assigns every response directly to the displayed result. I’ll add two isolated tests with controlled responses to verify both completion orders.


Reproduced a stale-response bug against actual `Search` at the component layer:

- Normal completion (`ca`, then `cat`): passes; latest result remains after both finish.
- Reversed completion (`cat`, then `ca`): fails; expected `'latest result'`, observed `'older result'`.

Saved `test_search.py` and `qa_controlled_fetch.py`. Tests capture request controls and real assertions, leave intermediate display unspecified, bound waits to 1 second, and cancel/drain owned tasks.

Rerun from the project root:

```sh
python3 -B -m unittest -v test_search
```

Result: **1 passed, 1 failed**. Production files and existing user changes were preserved.
