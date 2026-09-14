I’ll use the con-artist skill to trace the persistence path, run both tests against correct and faulty disposable copies, then strengthen the content assertions and repeat those checks.

Both tests assert only the acknowledgment dictionary. The real call path is `submit → FileStore.save → encode → Path.write_bytes`; the codec defaults to UTF-8 JSON.

I’ll replace the write argument with `b"{}"` in the faulty copy. This preserves encoding, file creation and acknowledgment while discarding the supplied content. Runtime diagnostics in both copies will confirm the loaded files, codec setting and bytes written.

The original tests both passed despite every write containing `{}`. The improved tests both pass on correct code and fail on the faulty copy at the persisted-content assertions; the acknowledgment assertions still pass.

The replacement test also starts with an extra field, so exact content equality checks that replacement removes obsolete data. I’ll now run the tests in the original project, verify file integrity and remove the disposable copies.

Confirmed the gap: both original tests accepted success without the supplied payload being persisted.

Traced `submit → FileStore.save → encode → write_bytes`. Runtime diagnostics confirmed copied module bindings and the effective JSON default (`STORE_CODEC` unset). The single isolated fault changed `write_bytes(payload)` to `write_bytes(b"{}")`.

All runs used `python3 -B -m unittest -v tests.test_submit`; both tests executed each time.

| Tests / implementation | Submission | Replacement | Exit |
|---|---|---|---|
| Original / correct copy | PASS | PASS | 0 |
| Original / faulty copy | PASS | PASS | 0 |
| Improved / correct copy | PASS | PASS | 0 |
| Improved / faulty copy | FAIL | FAIL | 1 |
| Improved / original project | PASS | PASS | 0 |

Updated `tests/test_submit.py` to read UTF-8 JSON and assert exact persisted content, retaining acknowledgment assertions. The detecting assertions were `self.assertEqual(persisted, …)`:

- Submission, line 14: actual `{}`, expected `{"title": "첫 요청", "count": 2}`.
- Replacement, line 22: actual `{}`, expected `{"title": "수정 요청", "count": 3}`.

Replacement also checks removal of an obsolete field through exact equality.

Integrity checks confirmed only `tests/test_submit.py` changed; production, README and skill resources were preserved. Scratch copies were removed, and `git diff --check` passed.

Evidence covers this single write-boundary fault and these payloads. Path hardening, concurrency and crash-atomic replacement remain outside scope.
