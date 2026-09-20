I’ll inspect the implementation and four tests, run both versions in separate disposable copies, and check their source identities and module origins while preserving the original files and Git state.

The tests already print the loaded module’s origin and process ID from the native test process. The source difference also points to a specific defect: HEAD consumes the length header before checking whether the payload is complete; the working tree keeps the header until the whole frame is available. I’ll now run all four unchanged tests against each version.

Verified with Node v24.16.0 using `node --test --test-reporter=tap tests/decoder.test.mjs` in two isolated project-local copies.

| Current test’s assertions (payloads shown as hex) | HEAD | Working tree |
|---|---|---|
| Split header: `[]`, then `['6869']` | Pass | Pass |
| Split binary payload: `[]`, then `['00ff0d0a']` | **Fail:** second push returned `[]` | Pass |
| Coalesced frames: `['61', '6263']` in order | Pass | Pass |
| Empty input, zero-length frame, empty input: `[]`, `['']`, `[]` | Pass | Pass |

HEAD’s own exit was **1** (3 passed, 1 failed); working tree’s was **0** (4 passed). HEAD reproduced an assertion failure, not a setup error.

Source identities:

- HEAD: `36bc8c44ffbbb459790fa2d62eae9b9c8e3a4e63`; decoder blob `691c2c9ee4972fc012eb22ee4a26c6d0ad257292`.
- Working-tree decoder SHA-256: `80e0b073fe75fe684f55293b3f895f56fba91453d743c2685b60b39b478c65a1`.
- Identical unchanged tests in both copies, SHA-256: `ade3786e4445be58b52660d172d2a73c00ae55a99b646862985ad6e576a82afb`.

The test-bound module reported its origin within the corresponding copy: `.decoder-verification-eE74Pu/HEAD/decoder.cjs` from native test PID **4147**, and `.decoder-verification-eE74Pu/working-tree/decoder.cjs` from PID **4149**. Both matched the expected absolute paths.

HEAD discards the two-byte header before checking payload completeness. In the failing case, the next push interprets payload bytes `00ff` as a new length of 255. The fix checks for all `2 + size` bytes before consuming anything, retaining incomplete frames correctly. All four tests support the fix; untested cases remain unverified.

All original file bytes/modes, including `notes.txt` and Git metadata, remained unchanged. HEAD, index, and Git status were preserved. All scratch was removed; no harness or report remains.
