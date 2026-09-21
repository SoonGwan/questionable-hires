I’ll use the necromancer skill to inspect the current contract, compare behavior using the local implementation, and trace the tenant dimension through pinned HEAD’s ancestry without editing the application.

**Do not remove `tenant` from the cache key.** `Catalog.lookup` (`catalog.py:10–14`) uses that key to decide whether to fetch. Returning only `item` violates `README.md:2`: “One Catalog may serve multiple tenants; item IDs are tenant-local.”

Using the specified interpreter with `-B`, I verified both imports resolved to this repository and exercised the actual `Catalog.lookup`, temporarily replacing only `cache_key` in memory.

| Requests, in order | Key implementation | Returned values | Fetch calls |
|---|---|---|---|
| east/17, west/17, east/17 | Current | `east:17`, `west:17`, `east:17` | east/17, west/17 |
| Same | Proposed | `east:17`, `east:17`, `east:17` | east/17 |
| east/17, east/18 | Current | `east:17`, `east:18` | east/17, east/18 |
| Same | Proposed | `east:17`, `east:18` | east/17, east/18 |

The proposal returns east’s cached value for west and suppresses west’s fetch. Both existing tests pass currently; under the proposal, `test_shared_catalog` fails and `test_single_tenant` passes. The single-tenant case cannot settle removal: its distinct item IDs never exercise a collision between tenants.

Historical evidence identifies **`a79c6a095450012ee6ff27ca345067b4c0df13b0`** (“Support shared catalogs across tenants”) as the introducing commit. Compared with its parent, `c6a8c060152df848f39a2c3be0185b1678684652`, it:

- Changed `return item` to `return (tenant, item)`, leaving `Catalog.lookup` unchanged.
- Documented shared catalogs and tenant-local IDs.
- Added both tests, including the shared sequence and fetch-call assertion.

`1a7537a164647952831f79571aceae76529a9026` is the merge, not the introduction. This establishes the historical change without assuming undocumented author intent; the current contract and reproduced failure independently establish present necessity.

Keep tenant isolation. No application edits were made. The substitution was restored; repository file bytes/modes, installed skill files, and HEAD were verified unchanged. No scratch was created, and history inspection stayed within pinned HEAD’s ancestors.
