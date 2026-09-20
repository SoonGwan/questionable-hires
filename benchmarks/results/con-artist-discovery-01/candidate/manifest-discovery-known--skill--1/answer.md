I’m using the con-artist skill to trace the checks’ actual writer binding, test an isolated missing-replacement fault, and verify the stronger byte comparison on both versions. I’ll preserve the originals and remove all audit scratch files.

Both success tests check only the returned acknowledgment. The call path is `test_engine.publish → bridge.refresh → bridge._install → engine.install`; the documented contract also requires replacement of the destination and pending-file cleanup.

I’ll trace that binding inside each native test process, then remove only `staged.replace(destination)` in a disposable copy.

The existing success tests **do not detect missing publication**. Both assert only the returned `{'published': version}` acknowledgment.

Same-process tracing confirmed `test_engine.publish is bridge.refresh`, `bridge._install is engine.install`, and execution of each disposable copy’s writer.

All runs used `python3 -B -m unittest discover -s checks -v`:

| Checks | Correct code | Replacement omitted |
|---|---|---|
| Existing tests | 2 passed; exit 0 | 2 passed; exit 0 |
| Existing + identical stronger check | 3 passed; exit 0 | 1 assertion failure; exit 1 |

The fault omitted only `staged.replace(destination)`, preserving acknowledgment and pending-file cleanup. The destination remained `b'previous manifest\n'`.

The stronger check seeded those different bytes, called the actual entrypoint, confirmed acknowledgment and `.pending` absence, then reopened the destination and compared its complete bytes against:

```python
'{"routes": ["/서울", "/café"], "version": 3}\n'.encode('utf-8')
```

This checks the documented ordering, separators, unescaped Unicode, UTF-8 encoding, and final LF. The faulty version failed specifically at byte equality—not during setup or import. Pending-file cleanup succeeded in both versions.

All original bytes and modes, including `notes.txt`, were verified unchanged. Disposable copies were removed; no production or test edits remain.
