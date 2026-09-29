I’m using the exorcist skill to test the cache explanation against the supplied client and loader. I’ll run the native tests and add a rerunnable probe with a JSON trace, keeping all supplied files unchanged.

The client keeps two root fields: `select_root` updates `root`, but `load` uses `_read_root`, set during construction. I’ll trace whether a beta request reaches the loader as an alpha path and causes another file read; that distinguishes stale path selection from a cached result.

The native tests pass both controls and fail the root switch (`111 != 222`). The probe shows why: after selecting beta, the same client still passes `alpha/settings.txt` to the loader, which opens and reads it again. The return to alpha passes, and a fresh beta client reads `222`; the other-filename checks show the same pattern.

The supported cause is stale root selection. `select_root()` updates `self.root`, but `load()` uses `self._read_root`, captured at construction.

Decisive trace event: requesting beta’s `settings.txt` passes **alpha/settings.txt** to the actual loader, which opens it, reads `"111\n"`, and returns `111`. A cached result is unnecessary to explain this reproduction.

- Native command `python3 -B -m unittest -v test_paths`: two controls pass; switching roots fails (`111 != 222`).
- One client, alpha→beta→alpha: settings return `111→111→111`; other filenames return `333→333→333`.
- A fresh beta client returns `222` and `444`.
- Every probed load performs a filesystem read.

Rerun with `python3 -B probe_paths.py`. The [probe](project/probe_paths.py) and [JSON trace](project/trace_paths.json) retain requested roots/filenames, loader inputs, opened file identities, read contents, and returned values.

Path resolution normalizes the selected root but does not update `_read_root`. The smallest corrective direction is to have `load()` use the current `self.root`. No fix was implemented; all 12 original files match their initial hashes.

This establishes the local mechanism only. Production behavior remains unobserved; filesystem reads also do not establish whether the OS served bytes from disk or its cache.
