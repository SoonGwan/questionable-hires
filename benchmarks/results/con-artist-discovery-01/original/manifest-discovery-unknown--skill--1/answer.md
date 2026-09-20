I’m using the con-artist skill to trace the tested call, run the controlled fault in disposable copies, and verify whether a complete-byte assertion detects the missing publication. I’ll preserve the originals and remove the copies afterward.


Both success tests assert only the returned `{'published': version}` acknowledgment. The tested path is `bridge.refresh` → its imported `_install` binding → `engine.install`. I’ll trace those bindings during the native test runs and omit only `staged.replace(destination)` in the fault copy, preserving the return value and cleanup.


The existing success tests **miss the omitted final replacement**. Both assert only the acknowledgment: `{'published': 2}` or `{'published': 3}`.

In-process tracing confirmed `test_engine.publish is bridge.refresh`, `bridge._install is engine.install`, and execution of the writer from each disposable copy. The fault omitted only `staged.replace(destination)`, preserving acknowledgment and pending-file cleanup.

All runs used `python3 -B -m unittest discover -s checks -v`:

| Checks | Correct code | Faulty code |
|---|---|---|
| Existing tests | 2 passed; exit 0 | 2 passed; exit 0 |
| Existing plus identical stronger assertion | 3 passed; exit 0 | 1 failure; exit 1 |

The stronger check seeded the destination with `b'previous manifest\n'`, called the actual entrypoint with a Unicode payload, reopened the destination, and compared complete bytes against:

```python
'{"routes": ["/서울", "/café"], "version": 3}\n'.encode('utf-8')
```

This checks sorted keys, unescaped Unicode, standard JSON spacing, and the final LF. Acknowledgment and `.pending` cleanup assertions passed on both versions. The faulty version failed specifically because the reopened destination still contained the seed bytes; there were no setup or import errors.

All original bytes and modes, including `notes.txt`, were verified unchanged. Disposable copies and instrumentation were removed; no production or test edits remain.
