# Friday phase defaults — native regression fix

The [interface model screen](FRIDAY-INTERFACE-MODEL-01-REVIEW.md) exposed a real
API failure under runtime `bef0937`: file-only phases omitted empty `sql`, so
the model rewrote and reran its entire probe. The original attempt is retained.

The new runtime accepts omitted `files` as `[]` and omitted `sql` as `""`.
Only a nonempty `name` is required; name alone is an observation checkpoint.
Unknown keys, explicit nulls and wrong types still fail. File ordering, inline
SQL after files, input budgets, read-only checks and incomplete-result semantics
are unchanged. The recipe is not mutated; no normalization writes project files.

Native regression evidence:

- Before the runtime patch, the new file-only/inline-only/checkpoint test errors
  with the same `each phase requires name, files and sql` message: 32 matrix
  tests, one error, 0.390s.
- After the patch, 40 Friday tests pass in 0.887s. The new test compares omitted
  versus explicit defaults, native non-UTF-8/empty BLOB rows, CLI serialization,
  original recipe/file preservation and all three phase shapes.
- Negative controls reject missing names, typos, nulls and wrong types before
  database connection. Oversized inline/file input and escaping file paths are
  also rejected before connection with optional fields omitted.
- Full local suite: **444 tests pass in 71.433s**, no failures or skips. Skill
  structure, repository links and featured-language synchronization checks pass.
  These are local validation results, not hosted CI or model performance.

This removes a demonstrated input-shape failure, not proven model overhead.
No fresh model measurement of this patch yet; do not subtract the old repair's
cost or replace old measurements with a hypothetical corrected run. Broader
20–30% savings remain unproven. No featured/chart changes are justified.
