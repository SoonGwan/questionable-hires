# Friday result reuse model screen 01 — reviewed

[Protocol](FRIDAY-RESULT-REUSE-MODEL-01-PROTOCOL.md), launch `2c5d98a`,
instructions `e0956d5`, runtime `e3bc342`. Both scheduled sessions complete;
no timeouts, exclusions or author retries. One exposed author task, n=1 per arm.

| Arm | Tokens (cached input included) | Seconds | Shell calls |
| --- | --- | --- | --- |
| Baseline | 66,530 | 64.128 | 3 |
| Skill | 92,665 | 65.436 | 6 |

**+39.28% tokens / +2.04% time** is adverse, not an efficiency win. Do not compare
this against earlier adverse pairs as a controlled causal old/new estimate.
Shared host/cache, unequal work and n=1 limit inference; no dollar estimate.

## Baseline review

Reads all original files and executes actual query modules via runpy after source
inspection. One in-memory SQLite loop executes initial/up/verification writes/down
and the active reader for each stage. Native output includes storage type/length/hex,
up roundtrip, current expected versus actual bytes for all four required payloads,
same current IDs, schema, encoding, integrity and unchanged original hashes.
Values/booleans are printed rather than asserted. It does not execute inactive
readers at every phase; these are not serving states under the explicit strategy.
Correct maintenance/recovery conclusions, no invented writer/staging evidence,
replacement migration or scratch. No observed scope/capture gap.

## Skill review

Reads entry, project and core guide; no advanced-guide or implementation read.
One discovery command also names absent `.codex` and exits with the visible
missing-directory error. It still lists the installed skill and continues; no
resource mutation or SQL repair is hidden.

**Uses the public matrix API once and reuses retained native rows** for all value
comparisons. No second migration loop or custom query extraction. File-only
phases omit empty SQL successfully. Complete native output contains four phases,
actual old/new reader references, inactive-reader errors, storage types/hex and
source/hash provenance. Assertions check completeness, successful untruncated
selected observations, BLOB/TEXT types, initial up roundtrip and current key sets.
Printed computed comparisons establish all four expected/actual byte values and
the nonempty mismatch/empty preservation pattern. ASCII hex recovery is computed
and printed true, not asserted. All project/installed files excluding Git are
hashed and the file set checked; no scratch or original changes.

The final byte table, faulty down transition, stopped-consumer strategy and
recoverability claims match native observations. Writer, operational and staging
evidence remains unknown. Required outcome is supported; extra all-reader checks
and broad hashes differ from baseline's integrity/schema/encoding work.

## Integrity and next decision

[Exports](results/friday-result-reuse-model-01/) retain every command, answer,
metadata and original snapshot. Author reconciliation confirms raw terminal usage,
sanitized events, frozen installed bytes and exact unchanged fixtures for both
cells with no errors. No observed native capture gap; audit is not model scoring.

The intended reuse behavior is observed but broad efficiency remains unproven.
Freeze this narrowly improved interface for now rather than repeatedly optimizing
the same exposed fixture. Next review other hires' real overhead/failure evidence;
future whole-bundle/independent tasks must test transfer. Historical/featured
measurements remain unchanged and no favorable isolated number is promoted.
