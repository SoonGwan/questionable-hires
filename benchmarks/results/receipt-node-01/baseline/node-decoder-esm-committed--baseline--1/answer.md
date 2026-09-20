I’ll inspect the source and four tests, then run them against HEAD^ and HEAD in separate disposable copies, checking each test-bound module’s origin and preserving the project state.

Verified: HEAD fixes the reproduced incomplete-payload defect.

Used Node v24.16.0 with `node --test --test-reporter=tap tests/decoder.test.mjs` in two separate project-local copies, containing actual revision sources and identical, unchanged current tests.

| Source revision | Native exit | Results |
|---|---:|---|
| HEAD^ `a69f3ea386eca20974476288825fe842825207d7` | 1 | 3 passed, 1 failed |
| HEAD `deaa42d06ba5a5ea476db830993d3115555d6f01` | 0 | 4 passed |

Working-tree `decoder.mjs` exactly matches HEAD.

The actual assertions compare emitted payloads as hex:

| Test | Expected successive results | HEAD^ | HEAD |
|---|---|---|---|
| Split header | `[]`, `['6869']` | Pass | Pass |
| Split binary payload | `[]`, `['00ff0d0a']` | Second result was `[]` | Pass |
| Coalesced frames | `['61', '6263']` | Pass | Pass |
| Empty frame and empty input | `[]`, `['']`, `[]` | Pass | Pass |

HEAD^ failed with `ERR_ASSERTION` at test line 16—a reproduced defect, with no setup or launch error.

Within the native test processes, the test-bound module reported these origins relative to the project:

- PID 99938: `.decoder-verification-3pyXou/parent/decoder.mjs`
- PID 99964: `.decoder-verification-3pyXou/head/decoder.mjs`

Both reported paths and resolved realpaths matched their corresponding copies. This is diagnostic source identity, not tamper-proof attestation.

HEAD^ removes the two-byte header before checking payload completeness. After a split payload, it interprets retained payload bytes as a new length. HEAD checks for all `2 + size` bytes before consuming anything, preserving incomplete frames. The loop then emits complete frames in order, including zero-length payloads.

All four tests ran in each copy without skips. Broader untested cases remain unverified. Snapshot comparison confirmed original file bytes/modes, `notes.txt`, Git HEAD/index, and existing untracked files unchanged. All scratch was removed; no harness or report remains.
