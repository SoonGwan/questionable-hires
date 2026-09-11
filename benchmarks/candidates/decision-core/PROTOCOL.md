# Decision-core experiment, not shipped skills

The default `skills/` tree remains unchanged. These two self-contained variants
keep the same names, descriptions, character lines and exact UI metadata. They
remove repeated procedural explanation while retaining maintenance-contract
reasoning, acceptance dependencies, scope, state recovery and verification.

Whitespace word counts including frontmatter: Landlord 300 → 180; Hostage
Negotiator 326 → 197. This is not a token/time result. Compact instructions may
omit useful nuance or increase model work; do not assume shorter means better.

Four unchanged existing cases are copied into `cases.json`: unnecessary formatter,
justified adapter, label-only edit with optional redesign, and necessary pending
state. Their original criteria stay intact. These are exposed development tasks,
not a confirmation set. They test both simplification and the refusal to simplify
away a required boundary/state. The full eight-skill objective remains unchanged.

Next run compares current shipped skills and these variants on identical requests,
one fresh Astra medium session per case/variant, serial, no retries or exclusions.
Use `--skills-root` to select this candidate without installing or replacing it.
Retain criteria outcomes, original changes, resource identities, rejected actions,
command traces and token/time totals. Schedule variant order in advance. A no-skill
comparison is still required before superiority claims; this experiment isolates
the choice between instruction variants, not model-versus-skill superiority.

Do not promote based on aggregate savings if a required control or scope condition
regresses. Inspect actual assertions and outcomes, not just completion messages.
No new helper, framework, delivery artifact or universal call-count rule is added.

## First scheduled comparison

Freeze both variants at `bb6bd5c` (the two shipped skill files and the isolated
candidate files). Eight sessions, four cases, one sample per variant; no no-skill
arm in this instruction-variant check. Order is fixed before execution:

1. formatter-review: shipped, candidate
2. adapter-justified: candidate, shipped
3. label-change: shipped, candidate
4. necessary-state: candidate, shipped

Use separate fresh `run.py` outputs for each case/variant, `--arms skill`, one
repeat, one job, Astra medium, seed 20260911, timeout 240 seconds. Compare installed
resources to frozen commit blobs afterward; do not edit either source tree during
execution. Stop on account limits or incomplete runner execution; do not restart
an observed failure to improve its score. This balanced order reduces one simple
order confound but does not make one repeat statistically conclusive.
