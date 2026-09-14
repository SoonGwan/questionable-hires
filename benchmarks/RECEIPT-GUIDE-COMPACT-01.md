# Receipt single-guide compaction — 2026-09-14

Previous source `94392cc`. Existing source-layout model evidence reads the full
`existing-fix.md` guide. This candidate removes repeated explanation while keeping
one guide, both executable examples, every input option, exit interpretation,
same-test constraints, selected-original integrity and process/budget limits.

Guide size: 6,215 → 5,713 bytes (**−8.08%**). SKILL.md, runtime, discovery metadata
and resource count are unchanged. This is byte arithmetic, not measured model
tokens, latency or task success. There is no new model run for this candidate.

A draft split into core/details was rejected: 5,486-byte core plus 2,307-byte
details would increase reading for the demonstrated `src/` task that needs both.
The draft detail file was removed before commit; no existing user file or
historical artifact was deleted. The retained single-guide examples continue to
execute actual committed and uncommitted comparisons with native before failure,
after success and unchanged originals. Do not trade required setup information
for an artificially short entry read.

Final candidate validation: 47 Receipt helper tests pass (15.019s), including
execution of both literal documented commands; 12 packaging tests pass (3.231s).
Repository validation, skill validation and EN/KO featured synchronization pass.

Follow-up: [single-guide adoption 01](RECEIPT-GUIDE-MODEL-01-REVIEW.md) measures
the committed candidate. It confirms use and observed before/after behavior on
one exposed task, not causal token/time improvement.
