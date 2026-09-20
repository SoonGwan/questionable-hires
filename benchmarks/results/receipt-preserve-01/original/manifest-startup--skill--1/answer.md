I’m using the receipt skill to compare both revisions with the current tests and startup configuration, while preserving the original workspace.


The change replaces delimiter splitting with CSV parsing. The five current tests cover quoted separators, escaped quotes, plain fields, empty fields and Unicode; they also verify both import paths inside the test process. I’ll use those checks with the documented runner and unchanged startup hook.


Verified: the committed CSV parsing change satisfies the requirements covered by all five current tests.

- Before: `dc1a0044e39c1af367031fce15027b9276caf7d5`
- After: `d973477c2b299730d2643a03f2ade52bb0c6e453`

Both disposable copies ran `PYTHONPATH=. python3 -B -m unittest -v test_manifest` with byte-identical current tests, startup hook and configuration.

| Test | Before | After |
|---|---|---|
| Quoted separator | Assertion failure: split inside quotes | Pass |
| Escaped quote | Assertion failure: retained enclosing/doubled quotes | Pass |
| Plain fields | Pass | Pass |
| Empty fields | Pass | Pass |
| Unicode | Pass | Pass |

Before exited **1** with two assertion failures; after exited **0**. No setup errors or skipped tests occurred.

Same-process checks confirmed `manifest.py` and `sitecustomize.py` loaded from `.receipt-native-743evf3f/before/` (PID 85165) and `/after/` (PID 85175), with the startup delimiter `;`.

`git diff --check` passed. All owned copies were removed; original file bytes, modes and symlinks—including user changes and ignored cache—were preserved. No harness or report remains.
