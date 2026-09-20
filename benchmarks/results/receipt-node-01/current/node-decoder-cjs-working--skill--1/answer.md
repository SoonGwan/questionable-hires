I’m using the receipt skill to compare HEAD with the working-tree decoder in disposable copies, run the same four tests, and verify the loaded module origins while preserving the project and Git state.


The change checks for a complete frame before consuming its header. HEAD consumes the header too early when a payload is split across chunks. I’ll use the supplied comparison helper to run both versions and check source identity and preservation.


Verified: HEAD reproduces the split-payload defect; the current working-tree implementation passes all four unchanged tests.

| Test | Actual assertions, frames shown as hex | HEAD | Working tree |
|---|---|---|---|
| split header | First byte → `[]`; remainder → `['6869']` | Pass | Pass |
| split binary payload | Header + first payload byte → `[]`; remainder → `['00ff0d0a']` | **Fail: returned `[]` on remainder** | Pass |
| coalesced frames | Combined frames → `['61', '6263']` in order | Pass | Pass |
| empty frame and empty input | Empty input → `[]`; zero-length frame → `['']`; empty input → `[]` | Pass | Pass |

Both ran with Node **v24.16.0**, using `node --test --test-reporter=tap --import <copy-local observer> <copy>/tests/decoder.test.mjs`.

- **HEAD:** `36bc8c44ffbbb459790fa2d62eae9b9c8e3a4e63`; native exit **1**, 3 passed / 1 failed.
- **Working-tree decoder SHA-256:** `80e0b073fe75fe684f55293b3f895f56fba91453d743c2685b60b39b478c65a1`; native exit **0**, 4 passed.
- Neither run skipped tests or encountered setup errors. The comparison helper separately exited **0**.

The test-bound module reported origins under project-local `.receipt-x821ykxh/before/decoder.cjs` in PID **2791** and `.receipt-x821ykxh/after/decoder.cjs` in PID **2793**. Each matched the loader’s path, PID and copied-source hash within its native process. This is diagnostic provenance, not tamper-proof attestation.

HEAD discards the two-byte header before confirming the payload is complete. On the next chunk, payload bytes become a mistaken length header. The fix checks `pending.length < 2 + size` before consuming anything, retaining incomplete frames intact. These observations verify the supplied cases; untested inputs remain unverified.

The whole-project preservation check passed, including supplied bytes/modes, `notes.txt`, Git HEAD and index. `git diff --check` exited **0**. All disposable copies and observers were removed; no harness or report remains.
