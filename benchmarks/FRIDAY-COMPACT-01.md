# Friday compact candidate — 2026-09-14

Previous resource: `7f5a1fc`. This is a candidate, not a measured model improvement.

Checkpoint 08's Friday skill used 108,299 tokens versus 83,973 baseline. Its
recorded path read the entry and core interface, then executed one matrix with
eight reader observations, full values/column assertions and static provenance.
No implementation read or repeated matrix execution explains that overhead.
The arms did different work; this is not causal attribution of the token gap.

## Change

- Entry text: 3,314 → 2,584 UTF-8 bytes (**−22.03%**), retaining actual rollout
  strategy, version resolution, witness selection, state-sensitive evidence reuse,
  new writes before rollback, data recovery, execution routing and authority limits.
- Formatter: omit JSON separator whitespace, without dropping fields, rows,
  errors, column labels, truncation, completion or provenance. The retained
  checkpoint's matrix object is 1,543 → 1,424 ASCII bytes (**−7.71%**).
  Parsed JSON is identical. BLOB encoding and ASCII escaping remain unchanged.

These byte reductions are neither tokenizer measurements nor whole-task savings.
The helper does not execute fewer checks. Documentation compaction could change
model interpretation; behavioral adoption and token/time effects need a frozen
fresh comparison, including adverse results and unchanged obligations.

## Local checks

36 matrix tests pass (0.397s), including real additive compatibility, incompatible
rename, new data surviving rollback, named-column failure, BLOB values, incomplete
migration, denied writes, truncation and deadlines. The added retained-observation
test preserves all four phases, four failed readers and both source records.
12 packaging tests pass (3.324s), including the shipped Friday executable's actual
compatible/incompatible reader outputs. Repository validation and skill validation
pass. These controls validate runtime/results, not whether models follow the
compressed entry correctly. No historical result, score or chart is rewritten.
