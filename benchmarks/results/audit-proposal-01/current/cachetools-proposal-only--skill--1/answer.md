I’m using the con-artist skill to run the two native tests against each isolated regression, trace their failures or gaps, and verify that all original files remain unchanged.

The tests exercise different boundaries: `test_lru` checks which keys survive eviction, while `test_lru_getsizeof` inserts a value large enough to evict both existing entries, masking their eviction order. Neither test overwrites an existing key. I’ll check those gaps with isolated mutations and record the package loaded by each test process.

**Three combinations detected the fault; five survived.** Both correct-code tests passed (`OK`, exit 0). Each baseline was reused for that test’s four comparisons.

Each run used a separate process from its disposable copy root:

```sh
python3 -B -m unittest tests.test_lru.LRUCacheTest.test_lru -v
python3 -B -m unittest tests.test_lru.LRUCacheTest.test_lru_getsizeof -v
```

Instrumentation inside each test process verified that both the test and its bound `LRUCache` came from that copy. Test bodies remained unchanged.

| Isolated regression | Native test | Correct code | Faulty outcome and evidence |
|---|---|---|---|
| Read does not refresh recency | `test_lru` | Pass | **Detected**, exit 1. Inserting key 4 evicts key 2 instead of 3. At line 26, evaluating `self.assertEqual(cache[2], 2)` raises `KeyError: 2`. |
| Read does not refresh recency | `test_lru_getsizeof` | Pass | **Survived**, exit 0. Reads leave recency unchanged, but inserting size-3 value evicts both existing keys anyway. |
| Overwrite does not refresh recency | `test_lru` | Pass | **Survived**, exit 0. Every assignment inserts a new key; no overwrite is exercised. |
| Overwrite does not refresh recency | `test_lru_getsizeof` | Pass | **Survived**, exit 0. No existing key is overwritten. |
| Eviction selects most-recent key | `test_lru` | Pass | **Detected**, exit 1. Inserting key 3 evicts key 2 instead of 1. At line 19, evaluating `self.assertEqual(cache[2], 2)` raises `KeyError: 2`. |
| Eviction selects most-recent key | `test_lru_getsizeof` | Pass | **Survived**, exit 0. Trace confirms eviction order changes from 1→2 to 2→1; both paths leave only key 3, satisfying every assertion. |
| Constructor ignores `getsizeof` | `test_lru` | Pass | **Survived**, exit 0. This test supplies no size function. |
| Constructor ignores `getsizeof` | `test_lru_getsizeof` | Pass | **Detected**, exit 1. Line 48, `self.assertEqual(len(cache), 1)`, fails with `AssertionError: 3 != 1`. |

The two `KeyError` outcomes are **behavioral detections**, although unittest labels them `ERROR`: the wrong eviction removes a required key before an assertion evaluates its argument. They are not setup/import errors. The sizing detection is an ordinary assertion failure.

Mutations affected only `LRUCache`: remove read-time recency update; skip overwrite-time update while retaining new-key registration; select `next(reversed(self.__order))`; or omit `getsizeof` from the base-constructor call. Each copy contained only one regression.

The shared coverage gap is **overwrite recency**. The weighted test also cannot distinguish eviction order. A focused proposed scenario is:

```python
cache = LRUCache(maxsize=3, getsizeof=lambda x: x)
cache[1] = 1
cache[2] = 2
cache[1] = 1                 # overwrite without an intervening read
cache[3] = 1
self.assertEqual(set(cache), {1, 3})
```

A separate version replacing the overwrite with `cache[1]` targets read refresh and eviction direction under weighted capacity. These suggestions are **unexecuted proposals**, not verified repairs. Constructor sizing is already protected by the existing weighted test.

All disposable copies and instrumentation were removed. The before/after inventory confirmed unchanged original file contents and modes, including license and metadata files.
