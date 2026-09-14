I’m using the con-artist skill to trace the write path, test one isolated persistence fault, and strengthen the persisted-content assertions. I’ll keep all scratch copies inside this project and remove them afterward.

Both tests currently assert only the acknowledgment. The write path is `submit → FileStore.save → encode → write_bytes`; the default codec is UTF-8 JSON. I’ll replace the write argument with `b"{}"` in a disposable copy, keeping encoding and acknowledgment intact, to check whether the tests detect lost payload content.

The original tests both passed while the faulty copy persisted `{}`. The improved tests both pass on correct code and fail on that fault at the new JSON-content assertions; the acknowledgment assertions still pass. Runtime traces confirmed the copied implementations, real bindings, and effective JSON codec were exercised. I’ll now check the final project and remove the scratch copies.

Confirmed the gap: both original tests accept successful acknowledgments even when supplied content is discarded.

Updated [tests/test_submit.py](project/tests/test_submit.py) to read `ticket.json` as UTF-8, decode JSON, and assert complete content after submission and replacement. Existing acknowledgment assertions remain.

Traced `submit → FileStore.save → encode → write_bytes`. Runtime evidence confirmed real copied bindings and the effective JSON codec. The sole fault changed `write_bytes(payload)` to `write_bytes(b"{}")` in the disposable copy.

Every run used `python3 -B -m unittest -v tests.test_submit`:

| Tests | Correct copy | Faulty copy |
|---|---|---|
| Original | Both pass; exit 0 | Both pass; exit 0 |
| Improved | Both pass; exit 0 | Both fail; exit 1 |

Both failures were content-equality assertions, with actual `{}` versus expected:

- Submission: `{"title": "첫 요청", "count": 2}`
- Replacement: `{"title": "수정 요청", "count": 3}`

The final original-project run also passed both tests; `git diff --check` passed. Integrity checks confirmed only `tests/test_submit.py` changed, and all scratch copies were removed.

This verifies detection of the selected content-loss fault. Other faults, concurrency, path hardening, and crash-atomic replacement remain outside this audit.
