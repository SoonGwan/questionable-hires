I’ll use the con-artist skill to trace the tested call and writer binding, then compare correct and faulty code in disposable project copies. I’ll preserve the originals and remove the copies afterward.


Both success tests assert only the returned acknowledgment. They call `bridge.refresh`, which uses the imported `engine.install`; neither checks destination bytes or pending-file cleanup.

I’ll omit only the final `replace` call in the faulty copy and trace that binding during the native test runs. If the tests still pass, I’ll add the same destination-bytes and cleanup assertions to both disposable copies.


The existing tests passed with replacement omitted. The stronger check passed on correct code and failed on the faulty code because the destination still contained `previous manifest\n`; acknowledgment and cleanup assertions passed.

The startup tracing hook did not load, so those runs lack the requested runtime binding evidence. I’ll rerun with tracing explicitly imported by the disposable checks.


The existing success tests **do not detect missing publication**. Both assert only `{'published': version}`.

In-process tracing verified copied imports and actual calls: `test_engine.publish → bridge.refresh → bridge._install`, with `_install is engine.install`.

All runs used `python3 -B -m unittest discover -s checks -v`:

| Checks | Correct code | Replacement omitted |
|---|---|---|
| Existing | 2 passed; exit 0 | 2 passed; exit 0 |
| Existing + stronger assertion | 3 passed; exit 0 | 1 failed, 2 passed; exit 1 |

The isolated fault omitted only `staged.replace(destination)`, preserving staging, acknowledgment, and cleanup.

The identical stronger check seeded `b'previous manifest\n'`, called the actual entrypoint with Unicode routes, reopened the destination, and compared complete bytes against:

```python
'{"routes": ["/서울", "/café"], "version": 3}\n'.encode('utf-8')
```

This checks the documented key order, separators, Unicode encoding, and final LF. Acknowledgment and `.pending` cleanup assertions passed on both versions. The faulty version failed specifically at byte equality because the old destination remained—not because of setup, import, or runner errors.

All original file bytes and modes, including `notes.txt`, were verified unchanged. Disposable copies were removed; no production or test edits were retained.
