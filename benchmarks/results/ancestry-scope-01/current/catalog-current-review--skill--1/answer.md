I’ll read the necromancer skill, current implementation, and contract, then compare both cache keys using the specified interpreter. I’ll keep this to a local review and leave the application unchanged.


The documented contract allows one `Catalog` to serve multiple tenants with tenant-local item IDs. `Catalog.lookup` uses `cache_key` to decide whether to fetch, and the shared-catalog test expects separate east and west results. I’ll now run both requested sequences with the current key and an in-memory replacement that returns only `item`.


**Keep `tenant` in the cache key.** Removing it breaks the current contract: [README.md](project/README.md#L2) allows one Catalog to serve multiple tenants whose item IDs are tenant-local. [Catalog.lookup](project/catalog.py#L10) uses that key to decide whether to fetch.

Observed using the actual local `Catalog.lookup`:

| Lookups | Key | Returned values | Fetch calls |
|---|---|---|---|
| east/17, west/17, east/17 | Current | `east:17`, `west:17`, `east:17` | east/17, west/17 |
| Same sequence | Proposed | `east:17`, `east:17`, `east:17` | east/17 |
| east/17, east/18 | Current | `east:17`, `east:18` | east/17, east/18 |
| Same sequence | Proposed | `east:17`, `east:18` | east/17, east/18 |

With the proposed key, west/17 receives east’s cached value without fetching west’s data. The single-tenant case passes because its item IDs differ; it never exercises a collision between tenants and therefore cannot establish contract preservation.

Both existing tests pass currently. With the substitution, [the shared-catalog test](project/test_catalog.py#L5) fails and the single-tenant test passes.

Used the specified interpreter with `-B`, verified local imports, and restored the in-memory substitution. Repository bytes/modes, HEAD, and installed skills were unchanged; no scratch remains. No history or network was accessed.
