# Friday compact entry candidate — 2026-09-14

Instruction revision `e063131`, compared with measured checkpoint-07 launch
`b2816cd`. Only skills/friday/SKILL.md changes; executable matrix, references,
metadata and task fixtures remain unchanged.

Checkpoint 07 adopted the matrix once without repair, yet Friday used 109,377
tokens versus baseline 103,365. Extra work differs and this does not identify
entry length as the causal overhead. The candidate reduces repeated instruction
prose, not required checks: 3,314 to 2,320 UTF-8 bytes (994 fewer, 29.99%). This is
file size, not measured token savings or model improvement.

Preserved decisions reviewed against the original entry:

- Actual release strategy/order and old/new artifacts determine reachable states;
  history resolves missing facts rather than becoming mandatory collection.
- New-version writes precede rollback inspection; code rollback, data reversal
  and evidenced restoration remain separate.
- Branches, representation boundaries and changed runtime state guide coverage;
  only unchanged evidence is reusable, not observations from before new writes.
- Application writers, transactions, connections and other engines require their
  actual runtime; the optional SQLite reader matrix is not a substitute.
- First incompatible/irreversible step, last recoverable state and compatible
  prerequisite remain the delivery. Missing evidence stays unknown, and review
  does not authorize deployment, edits or external staging actions.

Known artifact reads are grouped in the opening instruction. This may help avoid
redundant discovery but has no observed adoption result yet. No new universal
workflow, helper or fixture-specific example was added.

Skill frontmatter validation and repository link validation pass. The existing
full local suite completed 458 tests in 70.722s with no failures/skips during
this editing turn; it verifies code/packaging, not the revised instruction's
decisions or model efficiency. No wording-match test is presented as behavior.

Next validation should compare frozen old/new instructions on the same supplied
release artifacts, including a non-SQL application-writer path. Retain every
attempt and distinguish required evidence from extra work. Do not treat shorter
text or another favorable exposed pair as production performance proof.
