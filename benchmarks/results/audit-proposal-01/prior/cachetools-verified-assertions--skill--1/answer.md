I’m using the con-artist skill to run each isolated regression against both native tests, then verify stronger assertions for any gaps. I’ll use disposable project copies and check that all original files and modes remain unchanged.

Both tests omit overwrites. The weighted-size test also evicts both existing entries when inserting the size-3 value, so that step cannot distinguish which entry was least recent. I’ll verify those gaps and use a weighted insertion that evicts only one entry to check recency.

The existing tests detected **3 of 8 fault/test combinations**. All five surviving gaps were covered by executed stronger assertions that passed correct code and failed the corresponding isolated fault.

Each fault changed only `LRUCache`: removing read refresh; refreshing writes only for new keys; selecting the newest eviction key; or dropping the constructor’s `getsizeof` argument.

| Isolated fault | Native test | Correct code¹ | Faulty code | Detection or surviving gap |
|---|---|---|---|---|
| Read does not refresh | `test_lru` | PASS | ERROR, exit 1 | Line 26: evaluating `assertEqual(cache[2], 2)` raises `KeyError(2)` after insertion of key 4 wrongly evicts key 2. |
| Read does not refresh | `test_lru_getsizeof` | PASS | PASS, exit 0 | Reads do not change the insertion order; the subsequent size-3 insertion removes both old keys regardless. |
| Overwrite does not refresh | `test_lru` | PASS | PASS, exit 0 | No existing key is overwritten. |
| Overwrite does not refresh | `test_lru_getsizeof` | PASS | PASS, exit 0 | No existing key is overwritten. |
| Evict most recent | `test_lru` | PASS | ERROR, exit 1 | Line 19: evaluating `assertEqual(cache[2], 2)` raises `KeyError(2)` after insertion of key 3 wrongly evicts key 2. |
| Evict most recent | `test_lru_getsizeof` | PASS | PASS, exit 0 | Both old keys must be removed; their eviction order is unobservable. |
| Ignore supplied `getsizeof` | `test_lru` | PASS | PASS, exit 0 | No custom sizing function is supplied. |
| Ignore supplied `getsizeof` | `test_lru_getsizeof` | PASS | FAIL, exit 1 | Line 48: `assertEqual(len(cache), 1)` reports `3 != 1`. |

¹ Each native test’s successful correct-code run was reused across its four comparisons.

The two `ERROR` results are **behavioral detections**, not setup errors: the tests reached the stated assertion expressions, where incorrectly evicted keys were missing. Every process verified its copied `cachetools` import, test-local `LRUCache` binding, and constructor source path.

The following focused checks were executed as additional disposable unittest methods. `weighted(n)` below abbreviates `LRUCache(maxsize=n, getsizeof=lambda x: x)`.

| Gap covered | Executed setup and assertion | Correct result | Corresponding faulty result |
|---|---|---|---|
| Read refresh and MRU eviction in weighted test | `c=weighted(3); c[1]=1; c[2]=1; c[1]; c[3]=2; self.assertEqual(set(c), {1,3})` | PASS | Each fault independently FAILS: actual keys `{2,3}` |
| Overwrite refresh in default test | `c=LRUCache(2); c[1]=1; c[2]=1; c[1]=1; c[3]=1; self.assertEqual(set(c), {1,3})` | PASS | FAIL: actual keys `{2,3}` |
| Overwrite refresh in weighted test | Same overwrite sequence with `c=weighted(2)` | PASS | FAIL: actual keys `{2,3}` |
| Custom sizing absent from default test | `c=weighted(3); c[1]=1; c[2]=2; c[3]=2; self.assertEqual(set(c), {3})` | PASS | FAIL: actual keys `{1,2,3}` |

The first stronger check’s correct-code observation was reused for its two fault comparisons. All stronger failures were assertion failures, exit 1; all correct runs exited 0.

All 19 executions used `python3 -B -m unittest <selector> -v` from the relevant copy root. Original test bodies and other cache classes were unchanged. Disposable copies were removed, and the final integrity comparison confirmed all 68 original entries retained their contents and modes. No harness or report was left behind.
