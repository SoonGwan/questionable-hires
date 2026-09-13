I’ll use the mother-in-law skill to check the controller against the requirements, with controlled async sequences and the project’s test runner. I’ll preserve existing files and retain any QA tests under `tests/test_qa*.py`.


The existing tests cover normalization, deduplication, blank input, and retry after a `RuntimeError`. I’ll add checks for overlapping searches, repeated submissions, and clearing during pending work. I’ll also check an `OSError` failure: the requirements don’t restrict failure types, but the controller only catches `RuntimeError`.


Reproduced one defect: a current API failure using `OSError('connection lost')` escapes the search task and leaves `problem=None`. Expected: display `"connection lost"`. A subsequent successful retry works.

Passed: normalization, deduplication, `RuntimeError` recovery, overlapping success/failure completion orders, repeated queries, and clearing pending searches without late titles or errors reappearing.

Reproduction command from project root:

```sh
python3 -B -m unittest discover -s tests -t . -v
```

Result: 8 tests, 1 failing checkpoint. Added tests retained in `tests/test_qa_sequences.py`; existing files preserved.

Limits: actual Python controller tested with controlled API responses and 0.5-second async wait bounds. These do not bound blocking code. No browser, backend, external services, or dependencies used.
