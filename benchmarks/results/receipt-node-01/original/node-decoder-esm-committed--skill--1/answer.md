I’m using the receipt skill to compare both revisions with the unchanged current tests, verify which module each native test process loads, and remove the disposable copies afterward.

The fix delays consuming the header until the full payload is available. The current tests already print the imported module’s origin and process ID, so they can provide source identity evidence without modification. I’ll run the same four tests against each revision and capture each runner’s exit.

Verified: HEAD^ reproduces the payload-splitting defect; HEAD passes all four unchanged tests.

Both isolated copies ran Node v24.16.0 with:
```sh
node --test --test-reporter=tap tests/decoder.test.mjs
```

| Version | Revision | Native exit | TAP result |
|---|---|---:|---|
| HEAD^ | `a69f3ea386eca20974476288825fe842825207d7` | 1 | 3 passed, 1 failed |
| HEAD | `deaa42d06ba5a5ea476db830993d3115555d6f01` | 0 | 4 passed |

No tests were skipped. The failure was `ERR_ASSERTION`, not a setup error.

The actual assertions compared payloads as hexadecimal strings:

| Test | Expected push results | HEAD^ | HEAD |
|---|---|---|---|
| Split header | `[]`, then `['6869']` | Pass | Pass |
| Split binary payload | `[]`, then `['00ff0d0a']` | Second push returned `[]` | Pass |
| Coalesced frames | `['61', '6263']` | Pass | Pass |
| Empty frame/input | `[]`, then `['']`, then `[]` | Pass | Pass |

Within the native test processes, the test-bound module reported these origins, relative to the project:

- PID 1324: `.receipt-G9YBrF/before/decoder.mjs`
- PID 1334: `.receipt-G9YBrF/after/decoder.mjs`

Both resolved inside their corresponding copies and matched the respective revision’s bytes. Origin is diagnostic identity evidence. The working-tree implementation also matched HEAD byte-for-byte. Both test copies matched the current test file, SHA-256 `775e7b3a602145b4219a38c5f406b8d911ed73b53f8fee8bc5901f79963bc2ca`.

The old implementation consumed the two-byte header before checking payload completeness. On the next chunk, payload bytes were misread as a new length. HEAD checks for all `2 + size` bytes before consuming anything, preserving incomplete frames. These observations support the fix for the supplied cases; other payloads and chunk patterns remain unverified.

All supplied file bytes/modes, `notes.txt`, Git HEAD and index remained unchanged. Final diff checks exited 0; existing untracked state was preserved. All scratch was removed, leaving no harness or report.
