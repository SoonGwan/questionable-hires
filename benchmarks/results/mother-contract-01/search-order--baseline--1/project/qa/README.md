# Search overlap QA

Confirmed: an older response can replace the latest query's displayed result.
The user types `ca`, then `cat` while the first request is still pending. If
`cat` finishes first, its result appears correctly, but the late `ca` response
overwrites it. This violates `requirements.md`. Production `Search.run` assigns
each response without checking whether its query is still the latest.

Run from the project root (Python standard library only):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s qa -p 'test_search_overlap.py' -v
```

The current production implementation produces two tests: normal completion
passes, reversed completion fails with expected `results for cat`, actual
`results for ca`. Exit status 1 is expected while the defect remains. The test
does not mark this failure as expected or suppress the requirement assertion.
Actual controls, assertion values, traceback, and cleanup output from the run
are captured in `search_overlap_run.txt`.

The tests import the real `Search` and supply a local gated `fetch`. Events
confirm both requests have entered fetch in typing order; assertions confirm
both remain pending before either response is released. Futures control response
order without sleeps, networking, or scheduler timing assumptions. After the
first response, assertions check its visible result and that the other request
is still pending. After both responses, assertions check exact completion order
and that the latest query's result remains visible. Every behavior-dependent
wait has a two-second timeout. A `finally` block cancels and reaps all owned
request tasks and cancels unused gates, including on assertion failure.

`search.py` and `requirements.md` were preserved; their Git diff was empty
after verification. All added artifacts are under `qa/`.
