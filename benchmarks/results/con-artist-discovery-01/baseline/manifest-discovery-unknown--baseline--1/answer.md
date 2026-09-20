I’ll trace the tested entrypoint and writer binding, run the native tests, then compare correct and faulty code in disposable copies. I’ll preserve the originals and remove the copies afterward.


The success tests call `bridge.refresh`, which uses the `_install` function imported from `engine`. Both tests assert only the returned acknowledgment. They seed an old destination but never reopen it or check for a leftover `.pending` file.

I’ll trace those calls during the native test runs and omit only `staged.replace(destination)` in the faulty copy. The stronger check will verify cleanup and compare the reopened destination with literal expected UTF-8 bytes.


The existing success tests **do not detect missing publication**.

Same-process tracing confirmed the actual call chain: `test_engine.publish` → `bridge.refresh` → `bridge._install`, with `bridge._install is engine.install`. The writer paths pointed to the respective disposable copies.

Both existing tests assert only acknowledgments: `{'published': 2}` and `{'published': 3}`. Neither checks destination bytes or pending-file cleanup.

All runs used `python3 -B -m unittest discover -s checks -v`:

| Version | Checks | Result | Exit |
|---|---|---|---|
| Original | Existing | 2 passed | 0 |
| Correct copy | Existing, traced | 2 passed | 0 |
| Faulty copy | Existing, traced | 2 passed | 0 |
| Correct copy | Existing + stronger | 3 passed | 0 |
| Faulty copy | Existing + stronger | 2 passed, 1 assertion failure | 1 |

The isolated fault omitted only `staged.replace(destination)`, preserving acknowledgment and pending-file cleanup.

The identical stronger check seeded different destination bytes, called the actual tested entrypoint with Unicode data, verified acknowledgment and cleanup, then reopened the destination in binary mode and compared complete bytes against this literal encoded as UTF-8:

```python
'{"label": "경로", "routes": ["/서울", "/café"], "version": 7}\n'
```

This checks sorted keys, unescaped Unicode, standard separators, and final LF. The faulty version retained `b'previous DIFFERENT manifest\n'`, causing the byte-equality assertion to fail. This was **missing publication, not a setup or import error**. Pending-file cleanup passed on both versions.

Original file bytes and modes, including `notes.txt`, were verified unchanged. All disposable copies were removed; no production or test edits remain.
