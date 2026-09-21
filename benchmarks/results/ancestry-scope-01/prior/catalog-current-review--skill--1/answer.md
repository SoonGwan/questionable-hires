I’ll use the requested necromancer skill to review the current source, contract, and actual behavior, without inspecting history or editing the application.

**Keep `tenant` in the cache key.** Removing it breaks the documented contract: one Catalog may serve multiple tenants, and item IDs are tenant-local ([README.md](project/README.md#L2)). `Catalog.lookup` uses this key in its shared cache ([catalog.py](project/catalog.py#L10)), so the proposed key makes different tenants’ items collide.

Using the specified Python interpreter with `-B`, I verified local imports and exercised the actual `Catalog.lookup`, temporarily substituting only `cache_key` in memory and restoring it afterward.

| Lookups, in order | Key | Returned values | Fetch calls |
|---|---|---|---|
| east/17, west/17, east/17 | Current | `east:17`, `west:17`, `east:17` | east/17, west/17 |
| east/17, west/17, east/17 | Proposed | `east:17`, `east:17`, `east:17` | east/17 |
| east/17, east/18 | Current | `east:17`, `east:18` | east/17, east/18 |
| east/17, east/18 | Proposed | `east:17`, `east:18` | east/17, east/18 |

The proposed cleanup returns east’s cached value for west and skips west’s fetch. Both existing tests pass currently; with the substitution, the shared-Catalog test fails and the single-tenant test passes.

The single-tenant case cannot settle the decision because distinct item IDs never exercise a collision across tenants. Preserve tenant-specific cache identity; no application change is warranted.

Repository bytes/modes, skills, HEAD, and Git status/diffs remained unchanged. No scratch files were created, and no history or other refs were inspected.
