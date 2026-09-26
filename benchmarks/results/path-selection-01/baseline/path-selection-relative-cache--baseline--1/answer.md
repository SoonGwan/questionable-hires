I’ll inspect the supplied client and loader, run the native tests, and create a rerunnable probe that records loader calls and file reads without changing the supplied files.

All three native tests ran: the single-root and other-filename controls passed, and switching to beta returned `111` instead of `222`. The loader caches by filename while the client selects the root by changing the working directory. I’ll trace cache hits and file reads, including a fresh beta client, then clear only the in-memory cache and repeat the beta request to distinguish cache reuse from a root-selection failure.

Confirmed: the supplied loader’s cache key omits the root. `select_root` updates the root correctly, but `Client.load` passes only `"settings.txt"` to the module-level cached loader. Different clients share that cache.

All native tests ran with `python3 -B -m unittest -v test_paths`: **2 passed, 1 failed** (`test_switch_root`: `111 != 222`).

The probe recorded:

| Request | Physical read | Returned settings / other |
|---|---|---|
| Isolated alpha controls | Alpha files | 111 / 333 |
| Isolated beta controls | Beta files | 222 / 444 |
| Shared client: alpha | Alpha files | 111 / 333 |
| Same client: beta | None; cache hits | 111 / 333 |
| Same client: alpha again | None; cache hits | 111 / 333 |
| Fresh beta client | None; cache hits | 111 / 333 |
| Same fresh beta client after cache clear | Beta files | 222 / 444 |

**Discriminating observation:** the incorrect beta calls enter the loader with beta as the working directory, yet perform no file read. Clearing only the cache makes the identical requests read beta’s files and return the correct values. This supports filename-keyed cache reuse across roots and clients.

The smallest corrective direction is to pass the resolved root-plus-filename path into the cached loader, making file identity part of its key. No correction was implemented.

Rerun with `python3 -B probe_paths.py`:

- [Probe](project/probe_paths.py)
- [JSON trace](project/probe_trace.json)

The trace connects requested roots/filenames, actual loader arguments, working directories, file opens/reads, cache counters, and returned values. Supplied-file hashes remained identical; Git shows only the two new artifacts. These findings establish the local synthetic behavior; production behavior remains unverified.
