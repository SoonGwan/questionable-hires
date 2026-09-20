I’ll trace the entrypoint and writer used by the tests, then run the existing tests and stronger byte checks on disposable correct and faulty copies. I’ll preserve the originals and remove the copies afterward.

Both success tests assert only the returned acknowledgment. They call `bridge.refresh`, which uses the `_install` function imported from `engine`; the tests never reopen the seeded destination. I’ll verify that binding during execution and check whether omitting only `staged.replace(destination)` leaves the tests passing.

The existing success tests **do not detect missing publication**.

Same-process tracing confirmed the tested binding: `test_engine.publish` → `bridge.refresh` → `bridge._install is engine.install`. Correct runs reached the pending-file write, replacement, and cleanup; faulty runs reached write and cleanup but no replacement.

Both existing tests seed `b'previous manifest\n'` and assert only the acknowledgment (`{'published': 2}` or `{'published': 3}`). Neither checks destination bytes or pending-file cleanup.

All runs used `python3 -B -m unittest discover -s checks -v` in disposable copies:

| Checks | Correct code | Replacement omitted |
|---|---|---|
| Existing tests | 2 passed; exit 0 | 2 passed; exit 0 |
| Existing + identical stronger assertion | 3 passed; exit 0 | 1 failure; exit 1 |

The stronger check called the same entrypoint, reopened the seeded destination, and compared complete bytes against UTF-8 encoding of `'{"routes": ["/서울", "/café"], "version": 3}\n'`. This checks sorted keys, unescaped Unicode, standard separators, and final LF.

Acknowledgment and pending-file absence assertions passed on both versions. The faulty version retained `b'previous manifest\n'` and failed specifically at destination-byte equality—**missing publication, not a setup or import error**.

All original bytes and modes, including `notes.txt`, were verified unchanged. Disposable copies and instrumentation were removed; no production or test edits remain.
