I’m using the receipt skill to compare both revisions with the current tests and startup configuration, while preserving the original files and cache.


Verified: the committed `manifest.py` change satisfies the requirements exercised by all five current tests, replacing delimiter splitting with CSV parsing.

- Before: `dc1a0044e39c1af367031fce15027b9276caf7d5`
- After: `d973477c2b299730d2643a03f2ade52bb0c6e453`

Both disposable copies used identical current tests, `sitecustomize.py`, and `format.json`, running:
```sh
PYTHONPATH=. python3 -B -m unittest -v test_manifest
```

| Test | Before | After |
|---|---|---|
| Quoted separator | Assertion failure | Pass |
| Escaped quote | Assertion failure | Pass |
| Plain fields | Pass | Pass |
| Empty fields | Pass | Pass |
| Unicode | Pass | Pass |

Before returned `['a', '"b', 'c"', 'd']` for the quoted separator and `['a', '"b""c"', 'd']` for the escaped quote. These were actual assertion failures, not setup errors. Native exit codes were **1 before, 0 after**.

Same-process `NATIVE_IMPORTS` confirmed:
- PID **78189** loaded `before/manifest.py` and `before/sitecustomize.py`.
- PID **78193** loaded `after/manifest.py` and `after/sitecustomize.py`.

Both paths were under project-local `.receipt-native-x9y1xqws/`; startup assertions confirmed the configured `;` delimiter.

No requested evidence remains incomplete. All owned copies were removed. Original file contents and modes—including user changes and ignored cache—were unchanged; `git diff --check` passed.
