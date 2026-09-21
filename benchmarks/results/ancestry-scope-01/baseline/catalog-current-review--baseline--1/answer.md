I’ll inspect the current source and contract, then run both cache-key versions using the local implementation with an in-memory substitution that is restored afterward.

**The cleanup breaks the current contract.** README.md documents that one Catalog may serve multiple tenants and item IDs are tenant-local. `Catalog.lookup` uses `cache_key` to index its shared cache; returning only `item` makes different tenants’ items collide.

Observed using the actual local implementation:

| Sequence | Key | Returned values | Fetch calls |
|---|---|---|---|
| east/17, west/17, east/17 | Current `(tenant, item)` | east:17, west:17, east:17 | east/17, west/17 |
| Same | Proposed `item` | east:17, **east:17**, east:17 | east/17 |
| east/17, east/18 | Current | east:17, east:18 | east/17, east/18 |
| Same | Proposed | east:17, east:18 | east/17, east/18 |

The single-tenant case passes because distinct item IDs remain distinct keys. It does not exercise reuse of the same ID across tenants, which the documented contract permits.

Both existing tests pass currently; with the proposed key, the shared-catalog test fails and the single-tenant test passes.

Used the specified interpreter with `-B`, verified local imports, and restored the in-memory substitution. Repository bytes/modes and HEAD remained unchanged; no scratch files were created.
