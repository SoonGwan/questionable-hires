I’m using the receipt skill to compare both revisions with the unchanged current tests, verify which module each test process loads, and remove the disposable copies afterward.

HEAD^ reproduced the defect: the split binary payload test emitted `[]` instead of `['00ff0d0a']`. HEAD passed all four tests. Both native processes reported their corresponding copied module as the origin; the preservation check passed and the copies were removed.

Verified the existing fix with Node v24.16.0, using identical current tests in two project-local copies.

| Revision | Native exit | TAP result |
|---|---:|---|
| HEAD^ `a69f3ea386eca20974476288825fe842825207d7` | 1 | 3 passed, 1 failed |
| HEAD `deaa42d06ba5a5ea476db830993d3115555d6f01` | 0 | 4 passed |

Both ran `node --test --test-reporter=tap --import <copy-local observer> <copy>/tests/decoder.test.mjs`. Exactly four tests ran per version; none were skipped.

| Test | Actual assertions, expressed as output hex arrays | Before → after |
|---|---|---|
| split header | First byte → `[]`; remainder → `['6869']` | Pass → pass |
| split binary payload | Header plus one payload byte → `[]`; remainder → `['00ff0d0a']` | **Failed: got `[]` on remainder** → pass |
| coalesced frames | Combined frames → `['61', '6263']` | Pass → pass |
| empty frame and empty input | Empty input → `[]`; zero-length frame → `['']`; empty input → `[]` | Pass → pass |

The before failure was an assertion failure, not a setup error. HEAD^ consumes the length header before checking payload completeness. On the next chunk, it misinterprets retained payload bytes as a new header. HEAD checks for all `2 + size` bytes before consuming anything, preserving incomplete frames.

Same-process identity was confirmed by the unchanged tests’ `ACTUAL_MODULE` output and matching loader observations:

- Before, PID 2044: `.receipt-dylnwvqd/before/decoder.mjs`
- After, PID 2046: `.receipt-dylnwvqd/after/decoder.mjs`

Both paths were inside their respective project-local copies. Loaded source hashes matched the selected revisions; current working-tree decoder bytes also matched HEAD. The exported origin is diagnostic identity, not tamper-proof attestation.

The whole-project preservation check confirmed unchanged bytes/modes, including `notes.txt`, Git HEAD and index. All scratch was removed; no harness/report remains. Final diff checks passed. Behavior beyond these four tests was not independently exercised.
