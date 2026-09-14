# Friday phase defaults model screen 01 — reviewed

[Protocol](FRIDAY-PHASE-DEFAULTS-MODEL-01-PROTOCOL.md), launch `90d703a`,
runtime/instructions `e3bc342`. Both scheduled cells completed, no timeout,
exclusions or author retries. One exposed author task, n=1 per arm.

| Arm | Total tokens (cached input included) | Seconds | Shell calls |
| --- | --- | --- | --- |
| Baseline | 66,514 | 68.346 | 3 |
| Skill | 111,170 | 70.479 | 5 |

**+67.14% tokens / +3.12% elapsed time**, not an efficiency win. Shared host/cache,
one pair and unequal work prevent causal or broad performance claims. This is not
a controlled old-versus-new comparison; do not subtract the preceding repair cost.

## Baseline native evidence

Reads all seven original files; custom AST query extraction and in-memory SQLite
execute all four supplied stages. Both actual readers, schema and storage
type/length/hex observations are recorded. Explicit assertions verify initial
up roundtrip, exact expected current updated/untouched/empty/inserted payloads,
the nonempty mismatch pattern after down, same IDs and recoverability by ASCII
hex decoding. Original top-level file hashes unchanged; database closed.
No scratch or replacement migration. Final conclusion correctly rejects down's
representation, accepts the maintenance strategy's lack of overlap and avoids
irreversible-loss, staging or application-writer claims.

## Skill native evidence

Reads entry and core interface only. All four file-only phases omit `sql` and
complete on the first CLI call: **the corrected optional-field path is adopted
without the old preparation error**. Complete/untruncated native output covers
actual reader references, storage values/types/hex and all four stages, including
static source/hash provenance and BLOB JSON values.

Then writes a separate inline Python/AST/SQLite loop and executes the same four
migrations again for computed expected/current byte comparisons. This is extra
work, not an error retry. It asserts matching key sets and prints byte equality
and recoverability for every required payload; unlike baseline it does not assert
the exact expected values/mismatch pattern. File hashes cover project plus installed
resources, excluding Git. It leaves no scratch and does not alter originals.
The final byte table and maintenance/recovery conclusions agree with native output;
no invented staging or writer evidence.

This identifies another interface cost: the CLI observation and subsequent native
comparison use separate execution loops. The existing public API could supply
typed results for both, but was not selected. Future routing can make this choice
clearer; the current run does not prove that a different route would save tokens.

## Integrity and limits

[Exports](results/friday-phase-defaults-model-01/) retain both commands, native
outputs, answers, metadata and original snapshots. Author reconciliation confirms
terminal usage, sanitized raw events, unchanged installed resource bytes against
launch Git and exact fixture snapshots for both cells, with no errors. No observed
capture/scope gaps in manual review. These checks are not additional model success
scores. Historical adverse attempts and featured charts remain unchanged.
