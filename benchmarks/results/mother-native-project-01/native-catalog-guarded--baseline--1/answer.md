I’ll read the requirements and test setup, add QA tests in the permitted location, and run them to check normal behavior, recovery, and pending-search interactions.

The three existing tests pass. I’ll add deterministic checks for both completion orders, success/failure combinations, repeated identical queries, and clearing with multiple searches pending. I’ll also test `OSError`: the requirements describe failures generally, but the controller catches only `RuntimeError`.

QA completed: **9 tests passed, 1 failed**.

Reproduced defect: when the API raises `OSError("offline")`, the exception escapes `search()` and `problem` remains `None`. Expected: display `"offline"` as the current failure message. A subsequent successful retry works. The controller catches only `RuntimeError`.

Passing coverage includes normalization, title ordering/deduplication, empty results, RuntimeError recovery, overlapping distinct and identical queries in both completion orders, and clearing while multiple requests are pending.

Reproduce from the project root:

```sh
python3 -B -m unittest discover -s tests -t . -v
```

Retained tests in `tests/test_qa_catalog.py`. Existing files remain unchanged; no dependencies installed.

Limits: deterministic local API simulation only; no browser or backend. The defect assumes failures include `OSError`, since requirements do not restrict exception types.
