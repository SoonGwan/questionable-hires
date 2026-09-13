# Receipt entry consolidation after the frame comparison

Predecessor: `66313bf` (entrypoint originally `10d416f`). The
[frame comparison](results/receipt-frame-01/README.md) adopted final-check
batching and used three rather than six shell calls, yet recorded +4.01% tokens
and +9.81% time with the same required regression coverage. No optional resource
was loaded. This does not establish that entry length caused the difference.

The candidate consolidates repeated reuse/coverage/scope/stop explanations:
327 to 267 whitespace-delimited words, 2,425 to 1,987 file bytes. These are
source-size counts, **not tokenizer counts or model resource savings**. The
entry was already small; this edit alone is not a plausible demonstrated basis
for broad 20–30% improvement. It is a candidate requiring behavioral transfer,
not an accepted performance win.

Retained decisions: actual defect failure before a requested implementation;
unchanged assertions and matching runtime afterward; required neighboring
coverage; reuse invalidation when relevant inputs change; no skipped/undiscovered
test credit; no out-of-scope ancestor sweep; isolated historical comparison;
fail-fast final checks or explicit individual statuses; separate untracked-file
review; setup errors and mock limits; user-change and authorization boundaries;
concise evidence delivery and stop after the requested verification.

The executable final-check example is unchanged. Its four execution tests still
exercise success, test failure and whitespace failure paths with real subprocess
statuses. Catalog, skill schema, reference links and featured/localization checks
pass. These checks do not prove model adoption of the consolidated wording.
Description, automatic selection, helper resources and character are unchanged.
No additional reference load is introduced to hide the removed text.

Do not rerun the exposed frame task for a preferred score, rescore it, or update
featured images. Next behavioral validation needs a separate task with explicit
equivalent required work, frozen before execution. Whole-bundle and independent
real-developer confirmation remain necessary; compression is not their substitute.
