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

## Output-choice follow-up — 2026-09-14, previous source `da5b10e`

The measured model explicitly requested `--pretty`, despite an existing lossless
compact default. Clarify the guide's choice: agent execution uses default JSON;
indentation is for a human-readable JSON request. No runtime, schema, entrypoint
or integrity behavior changes. Do not add another formatter or remove original
preservation checks: the observed whole-tree wrapper also checks entries and Git
metadata, which the helper's selected-file guarantees do not cover.

On the retained `receipt-guide-model-01` item_5 helper object, the original
indented JSON is **6,036 UTF-8 bytes**; compact serialization is **5,516 bytes**,
**−8.61%**, excluding the following wrapper output and final newline. Full parsed
objects compare equal, including native failure/pass output, hashes, modes,
cleanup and exit fields. This is serialization arithmetic on recorded evidence,
not a new model run, token savings or proven adoption of the changed instruction.

Reproduce from the exported `commands.json`: select item_5, decode its leading
object with `json.JSONDecoder().raw_decode`, verify that the consumed substring
equals `json.dumps(value, indent=2)`, then compare against
`json.dumps(value, separators=(',', ':'))` in UTF-8 and assert parsed equality.

Validation after the wording change: 47 helper tests / 15.068s and 12 packaging
tests / 3.236s pass. The helper tests include actual native failing-before and
passing-after observations serialized through both CLI modes, with full object
equality. Skill/repository validation and featured EN/KO synchronization pass.
Model adoption and whole-task efficiency of this instruction remain unmeasured.

Subsequent [output-choice screen 01](RECEIPT-OUTPUT-CHOICE-01-REVIEW.md) observes
compact selection but **higher** recorded whole-task token/time cost. The candidate
validation above is historical pre-run evidence, not an efficiency claim.
