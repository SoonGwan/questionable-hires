I’ll read the requirements and test setup, add QA tests in the permitted location, and run them to check normal behavior, recovery, and pending-search interactions.

Stale successful responses appear to overwrite newer results and restore titles after clearing. The test helper also masks assertion failures because its `fail` method conflicts with unittest’s. I’ll adapt only the added QA test class so the failures report expected and observed values clearly.

Added 12 QA tests in `tests/test_qa_catalog.py`. **15 tests ran: 10 passed, 5 failed.** Existing files remain unchanged.

Reproduced one controller defect: successful responses update state without checking whether the search is still current (`catalog/controller.py:22`).

| Reproduction sequence | Expected | Observed |
|---|---|---|
| Latest succeeds, then older succeeds | Keep latest titles | Older titles overwrite them |
| Older succeeds while latest is pending | Preserve displayed state | Older titles appear |
| Latest fails, then older succeeds | Preserve latest error | Older titles appear and error clears |
| Clear while pending, then pending succeeds | Remain empty | Titles reappear |
| Clear, complete new search, then complete two older searches | Keep new results | Oldest results overwrite them |

Normalization, ordered deduplication, empty responses, failure messages, successful retry, immediate clearing without API calls, and stale-failure suppression passed.

Reproduce from the project root:

```sh
python3 -B -m unittest discover -s tests -t . -v
```

Limits: deterministic local controller tests using controlled futures, valid records, and `RuntimeError`; no browser/backend or exhaustive scheduling coverage. The existing helper’s `fail` method conflicts with unittest assertion reporting; the added QA subclass works around it without changing support code. No dependencies installed or external services used.
