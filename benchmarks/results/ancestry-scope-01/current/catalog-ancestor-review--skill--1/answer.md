I’ll use the local necromancer skill to inspect the contract and pinned history, then compare both cache keys against the actual implementation without changing application files.

**Keep the tenant dimension.** Returning only `item` breaks the documented contract: one Catalog may serve multiple tenants, and item IDs are tenant-local ([README.md](project/README.md#L2)). [`Catalog.lookup`](project/catalog.py#L10) uses the key in one shared cache, so the proposed key makes different tenants collide.

Using the specified interpreter with `-B`, I verified local imports and exercised the actual `Catalog.lookup`, temporarily replacing only `cache_key` in memory and restoring it afterward.

| Lookups | Key | Returned values, in order | Fetch calls, in order |
|---|---|---|---|
| east/17, west/17, east/17 | Current | east:17, west:17, east:17 | east/17, west/17 |
| Same | Proposed | east:17, **east:17**, east:17 | east/17 |
| east/17, east/18 | Current | east:17, east:18 | east/17, east/18 |
| Same | Proposed | east:17, east:18 | east/17, east/18 |

Both existing tests pass currently. With the proposed key, [`test_shared_catalog`](project/test_catalog.py#L5) fails; the single-tenant test passes. That single-tenant case cannot settle the decision because it never exercises equal item IDs across tenants.

Historical evidence, restricted to pinned HEAD `1a7537a164647952831f79571aceae76529a9026` and its ancestors:

- **Introducing commit:** `a79c6a095450012ee6ff27ca345067b4c0df13b0` (“Support shared catalogs across tenants”).
- Its parent, `c6a8c060152df848f39a2c3be0185b1678684652`, returned `item`. The introducing commit changed this to `(tenant, item)`, leaving the lookup consumer unchanged.
- The same commit added both tests and documented the shared-Catalog, tenant-local-ID contract.
- `1a7537a…` is the merge, not the introduction.

Those changes establish historical origin without assuming author intent. The current contract and reproduced wrong-tenant result independently establish present necessity. The smallest next action is to retain the existing key.

No application files were edited. Project and local skill bytes/modes and HEAD were verified unchanged; no scratch files were created.
