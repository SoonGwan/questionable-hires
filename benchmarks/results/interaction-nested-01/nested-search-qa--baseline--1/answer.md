I’ll inspect the project requirements and search code, then reproduce any sequence failure with focused QA tests in the project’s designated location.

The code applies every response when it arrives, which appears to let an older request overwrite a newer result. I’ll test controlled response ordering for overlapping searches and for clearing the query, plus a normal sequence that includes an empty query.

Found a deterministic stale-response failure: an older search overwrites the latest query’s results.

- Type `b`, then `book`; complete `book` first. Its `['book']` result is overwritten by the older `['book', 'bag']`.
- Type `b`, then clear the query; complete the empty query first. Its `[]` result is likewise overwritten.
- Normal sequential searches, including an empty query, pass.

Retained tests in `apps/catalog/qa/test_search.py`, importing the actual implementation and controlling completion order without sleeps. Original files unchanged; no dependencies installed.

Reproduce from `apps/catalog`:

```sh
python3 -B ../../tools/check.py --timeout 3 -- python3 -B -m unittest discover -s qa -p 'test_*.py' -v
```

Observed: **1 pass, 2 failures**. Runner JSON confirms `exit_code: 1`, `timed_out: false`, and `cleanup_complete: true`.
