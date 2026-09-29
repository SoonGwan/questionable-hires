I’ll inspect the supplied client and loader, run the native tests, and add a rerunnable probe and JSON trace while leaving all original files unchanged.

The two control tests pass; the root-switch test fails with `111 != 222`. The client keeps a separate `_read_root` initialized to alpha, and `select_root` updates only `root`. I’ll trace calls through the real loader and file reads to distinguish a wrong path from cached content, including the return to alpha that the failing test never reaches.

The supplied client retains its construction-time read root. `select_root()` updates `self.root`, but `load()` uses the unchanged `self._read_root`.

The discriminating observation: after selecting beta, the actual loader receives **alpha/settings.txt**, opens and reads it again, and returns `111`. This supports a stale path mechanism, not cached content.

| Scenario | Settings | Other filename |
|---|---:|---:|
| Single-root alpha controls | 111 | 333 |
| One client: alpha → beta → alpha | 111 → **111** → 111 | 333 → **333** → 333 |
| Fresh beta client | 222 | 444 |

Ran `python3 -B -m unittest -v test_paths`: **2 passed, 1 failed**, with `111 != 222` in the switching test.

Added [probe_paths.py](project/probe_paths.py) and [probe_trace.json](project/probe_trace.json). Rerun with `python3 -B probe_paths.py`. The trace connects each requested root/filename to the actual loader input, resolved file path and handle identity, read text, and returned value. All 10 calls performed a read.

Smallest corrective direction: have `load()` use the currently selected `self.root`. No correction was implemented; hashes and Git diff confirm all original files remain unchanged.

These findings establish the supplied local behavior. Production code, configuration, and behavior remain unknown.
