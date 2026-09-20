I’m using the con-artist skill to trace the checks’ actual writer binding, test an isolated missing-replacement fault, and verify the stronger byte-for-byte assertion. I’ll preserve the originals and remove all audit scratch.


Both success tests assert only the returned acknowledgment. The documented contract also requires destination bytes and pending-file cleanup. I’ll trace calls through `bridge.refresh` and its bound `engine.install` while running the checks, then verify whether omitting replacement leaves the old manifest behind despite passing tests.


The existing tests passed on both versions. Tracing confirmed that the faulty writer returned success and removed `.pending`, but left the destination unchanged. My first disposable stronger check had a string-escaping syntax error, so its exits are setup errors, not evidence of detection. I’ll correct that check and rerun it on both versions.


The existing success tests **do not detect missing final replacement**.

Same-process tracing confirmed the executed path: `test_engine.publish` → `bridge.refresh` → `bridge._install`, bound to the copied `engine.install`. The isolated fault omitted only `staged.replace(destination)`, preserving acknowledgment and pending-file cleanup.

All runs used `python3 -B -m unittest discover -s checks -v`:

| Checks | Correct code | Faulty code |
|---|---|---|
| Existing tests | 2 passed; exit 0 | 2 passed; exit 0 |
| Existing + stronger assertion | 3 passed; exit 0 | 1 assertion failure; exit 1 |

The existing assertions compare only `{'published': 2}` and `{'published': 3}`. Neither checks destination contents or cleanup.

The identical stronger check seeded `b'previous manifest\n'`, called the actual entrypoint with Unicode routes, reopened the destination, and compared complete bytes against:

```python
'{"routes": ["/서울", "/café"], "version": 3}\n'.encode('utf-8')
```

This verifies the documented ordering, separators, Unicode encoding, and final LF. Acknowledgment and `.pending` absence passed on both versions. The faulty version failed specifically because the destination retained the seeded bytes.

An initial disposable check had a syntax error on both versions; those setup failures were excluded and corrected before the decisive runs.

All original file bytes and modes, including `notes.txt`, were verified unchanged. Disposable copies were removed; no production or test edits remain.
