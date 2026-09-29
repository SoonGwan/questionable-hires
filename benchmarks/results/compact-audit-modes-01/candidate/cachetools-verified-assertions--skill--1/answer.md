I’ll use the con-artist skill to run each regression in an isolated copy, check both native tests, and verify stronger assertions for any surviving gaps. I’ll preserve the originals and remove the disposable copies afterward.


The plain test exercises read recency, but neither test overwrites an existing key. The weighted test also evicts both old entries at once, which may hide an incorrect eviction order. I’ll check those gaps with isolated faults and assertions that leave one old entry in the cache.


The first baseline test passed, but Python didn’t load the import-verification hook. That leaves provenance unverified, so I’m not counting it as an audit baseline. I’ve removed that copy and will rerun with the copied root explicitly on Python’s startup path.


The existing tests detected **3 of 8 fault/test combinations**. Five gaps survived; all five are covered by stronger assertions that I executed successfully on correct code and confirmed fail on the corresponding faults.

Each regression occupied a separate copy and changed only `LRUCache`: removing read refresh, refreshing writes only for new keys, selecting the newest eviction candidate, or omitting the constructor’s `getsizeof` argument.

| Fault | Native test | Correct code | Faulty code and decisive evidence |
|---|---|---|---|
| 1. Reads don’t refresh | `test_lru` | PASS | **Detected:** line 26, `assertEqual(cache[2], 2)`, raises `KeyError: 2` after inserting key 4. |
| 1. Reads don’t refresh | `test_lru_getsizeof` | PASS | **Survives:** reads leave the original order unchanged overall; the subsequent insertion evicts both old keys. |
| 2. Overwrites don’t refresh | `test_lru` | PASS | **Survives:** no existing key is overwritten. |
| 2. Overwrites don’t refresh | `test_lru_getsizeof` | PASS | **Survives:** no existing key is overwritten. |
| 3. Evicts most recent | `test_lru` | PASS | **Detected:** line 19, `assertEqual(cache[2], 2)`, raises `KeyError: 2` after inserting key 3. |
| 3. Evicts most recent | `test_lru_getsizeof` | PASS | **Survives:** inserting size 3 requires removing both old keys, hiding eviction order. |
| 4. Ignores supplied size function | `test_lru` | PASS | **Survives:** no custom size function is supplied. |
| 4. Ignores supplied size function | `test_lru_getsizeof` | PASS | **Detected:** line 48, `assertEqual(len(cache), 1)`, fails with `3 != 1`. |

The two `KeyError` results are behavioral detections during assertion argument evaluation, reported by unittest as `ERROR`; they are not setup errors.

These focused checks were added only in disposable modules. Operations below execute left to right; “weighted” means `LRUCache(maxsize=3, getsizeof=lambda x: x)`.

| Gap covered | Executed setup and assertion | Correct outcome | Corresponding faulty outcome |
|---|---|---|---|
| Fault 1, weighted test | Weighted; `c[1]=1; c[2]=2; c[1]; c[3]=1`; `self.assertEqual(set(c), {1,3})` | PASS: `{1,3}` | FAIL: `{2,3}` |
| Fault 2, both tests | `LRUCache(maxsize=2)`; `c[1]=1; c[2]=2; c[1]=10; c[3]=3`; `self.assertEqual(set(c), {1,3})` | PASS: `{1,3}` | FAIL: `{2,3}` |
| Fault 3, weighted test | Weighted; `c[1]=1; c[2]=2; c[3]=1`; `self.assertEqual(set(c), {2,3})` | PASS: `{2,3}` | FAIL: `{1,3}` |
| Fault 4, plain test | Weighted; `c[1]=2`; `self.assertEqual(c.currsize, 2)` | PASS: `2` | FAIL: `1` |

The overwrite check supplies the missing contract for both overwrite gaps; its single correct/faulty pair is shared evidence.

All verified executions used `python3 -B -m unittest <selector> -v` from copy roots. A same-process hook verified copied package/test paths and their `LRUCache` bindings. Each native baseline ran once and was reused across four comparisons: **10 verified native executions plus 8 stronger-check executions**. One earlier baseline passed without the provenance hook loading; it was excluded and rerun after correcting the startup path.

Original paths, file bytes, and modes matched the initial inventory after cleanup. All disposable copies and checks were removed; no permanent harness or report remains.
