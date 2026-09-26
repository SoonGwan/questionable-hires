I’ll use the exorcist skill to test whether the client passes the selected root to the loader, then record file reads and results without changing any supplied files.

The client changes directories but passes only the filename to a shared `lru_cache`. I’ll trace whether a beta request reaches the file read, and use a cache-cleared beta request to distinguish a cache-key collision from an incorrect root selection. The supplied tests cover both normal controls and the reported switch failure.

Confirmed a **cache-key collision** in the supplied implementation: the client changes directories but passes only `"settings.txt"` to the module-level `lru_cache`. The selected root is absent from the key, and fresh clients share that cache.

- Native command `python3 -B -m unittest -v test_paths`: 3 tests ran; both controls passed, root switching failed (`111 != 222`).
- One client’s alpha→beta→alpha results: **111→111→111**. Beta caused no file read.
- A fresh beta client also returned **111** without reading.
- **Discriminating observation:** clearing only the cache, keeping the beta client/root/filename fixed, caused an actual beta file read and returned **222**. Other-filename controls were retained.

The `finally` block correctly restores the working directory, but cannot distinguish identical filename cache keys across roots.

Smallest corrective direction: pass the resolved root-qualified file path to the cached loader so file identity participates in its key. No fix was implemented.

Rerun: `python3 -B experiments/probe_paths.py`. The [probe](project/experiments/probe_paths.py) delegates to the actual client and loader; its [JSON trace](project/experiments/paths_trace.json) records requests, loader inputs, cache statistics, physical reads, and returned values. Hash checks confirmed all original files unchanged.

This establishes the mechanism in this sequential local project; production behavior remains unobserved.
