# Bulk-history transfer development check

Two new synthetic development cases from `history_transfer_cases.py`, not a
confirmation set: identical large contiguous history, with either a still-active
fallback or a sole caller that now normalizes records. The fixed request requires
historical attribution and actual current/proposed renderer behavior on missing,
empty and nonempty display values. Review only; no project edits. Criteria are
frozen before sessions. Author fixture checks establish both behavior outcomes
and that the selected historical addition lies beyond the old patch prefix.

Use current shipped skills, Astra medium, one fresh session per case/arm, serial,
timeout 240 seconds, seed 20260911, no retries/exclusions. Four sessions:

1. history-bulk-active baseline
2. history-bulk-active skill
3. history-bulk-normalized skill
4. history-bulk-normalized baseline

Freeze the implementation and fixture commit before running; generate a fresh
ignored cases JSON for run.py. Preserve original traces, file/resource identities,
failed actions, verification depth and input-plus-output tokens (cache included).
Inspect helper use and follow-up commands; do not require the optional helper or
force its use to manufacture adoption. Native Git may be sufficient. These pairs
compare current skill with no skill, not old versus new collector causally.
Do not infer superiority from one repeat or equal conclusion alone. Retain both
cases even when the control or costs are unfavorable. The original benchmark and
the full eight-skill performance objective remain unchanged.
