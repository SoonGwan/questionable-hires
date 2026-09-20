I’m using the receipt skill to compare HEAD and the working-tree decoder in disposable local copies, with the same four tests. I’ll verify which module each native test process loads, preserve the original files and Git state, and remove the scratch copies afterward.


The change checks for the full header and payload before consuming any bytes. The four tests cover a split header, a split binary payload, coalesced frames, and empty frames/input. They already print the module’s origin and process ID, so I can verify the loaded copy without changing them.


Verified: HEAD reproduced the split-payload defect; the unstaged fix passed all four unchanged tests.

Both isolated copies ran Node v24.16.0 with:
```sh
node --test --test-reporter=tap tests/decoder.test.mjs
```

| Test | Actual assertions (payloads in hex) | HEAD | Working tree |
|---|---|---|---|
| Split header | First chunk → `[]`; remainder → `['6869']` | Pass | Pass |
| Split binary payload | First chunk → `[]`; remainder → `['00ff0d0a']` | Failed: remainder returned `[]` | Pass |
| Coalesced frames | One push → `['61', '6263']` | Pass | Pass |
| Empty frame/input | Empty input → `[]`; zero-length frame → `['']`; empty input → `[]` | Pass | Pass |

HEAD’s native runner exited **1** (3 passed, 1 failed); working tree exited **0** (4 passed). Neither run skipped tests or encountered setup errors.

Source identities:
- HEAD: `36bc8c44ffbbb459790fa2d62eae9b9c8e3a4e63`
- HEAD decoder blob: `691c2c9ee4972fc012eb22ee4a26c6d0ad257292`
- Working decoder SHA-256: `80e0b073fe75fe684f55293b3f895f56fba91453d743c2685b60b39b478c65a1`
- Identical current test SHA-256: `ade3786e4445be58b52660d172d2a73c00ae55a99b646862985ad6e576a82afb`

Within each native test process, the test-bound module reported its origin under the corresponding project-local copy: `.receipt-vn3lsg/HEAD/decoder.cjs` (PID 3495) and `.receipt-vn3lsg/working-tree/decoder.cjs` (PID 3497). Both resolved to the expected copied files. This is diagnostic source identity.

HEAD consumes the two-byte header before checking payload completeness, losing framing across chunks. The fix checks `pending.length < 2 + size` first, retaining the complete partial frame. The observed regression supports that mechanism; arbitrary payloads and chunk arrangements beyond these tests remain unverified.

All 55 inventoried project entries retained their bytes/modes, including `notes.txt`, Git HEAD and index. `git diff --check` exited 0. All scratch was removed; no harness or report remains.
