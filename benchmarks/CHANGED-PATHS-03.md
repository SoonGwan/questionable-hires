# Changed paths 03: Friday token reduction, Receipt overhead remains

[Frozen protocol](CHANGED-PATHS-03-PROTOCOL.md), snapshot `eefe278`, Receipt
`7056153`, Friday `9cae27c`, runner `fd8d578`. Two unchanged exposed development
tasks, four fresh Astra medium sessions, serial, seed 20260911, 240-second limit.
Actual order: rolling skill, boundary skill, boundary baseline, rolling baseline.
No retries, exclusions, timeouts or candidate changes during execution. Raw
captures remain private in `benchmarks/local-runs/changed-paths-03`.

| Case | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| Boundary fix | 79,274 / 30.285 | 102,462 / 52.785 |
| Rolling schema | 78,935 / 39.084 | 68,323 / 39.092 |
| Sum | 158,209 / 69.369 | 170,785 / 91.877 |

Total tokens are input (including cache) plus output. Skill sum is +7.9% tokens /
+32.4% time: no combined performance acceptance. Friday alone uses 13.4% fewer
tokens with effectively equal observed time; Receipt is costlier. One sample,
exposed tasks, unequal verification and shared host/cache prevent stable or causal
claims. This is neither a whole-bundle result nor independent confirmation.

## Actual behavior

Boundary arms produce identical two-file diffs: >=18 and one age-18 regression,
retaining ages 17/19. Both original logs show the same assertion failing before
and all three passing after. Neither duplicates the targeted regression outside
the suite. Baseline uses four shell commands; skill seven. Skill additionally
reads its entrypoint, searches existing files for runner evidence and separates
final checks. It runs `git diff --check` in an initial semicolon chain and again
alone after the suite, with no intervening source edit. The first chain's final
status does not isolate the whitespace check's exit; do not claim the second run
is necessarily redundant *evidence*. It is repeated computation whose status
could instead be retained when first collected. The original standalone check is
quiet with exit zero, accounting for the one empty-output diagnostic.

Both schema arms execute the supplied queries and migrations in in-memory SQLite,
show old-reader failure after up/old-binary-first rollback and new-reader failure
after down, reject the documented order and propose compatible staging. Neither
certifies untested runtime readiness. Skill adds a post-up insertion and asserts
both old/new-data rows survive down; baseline checks one original row only. Skill
does not use/read the optional matrix helper, and no history lookup occurs. Both
use four shell commands, though baseline's first AGENTS-only discovery returns 1
and requires another listing. Fewer commands alone does not explain Friday's
token difference; per-command model usage is unavailable.

## Integrity and direction

Original commands, outputs, answers and diffs were inspected. Twelve schema file
instances remain unchanged; schema diffs are empty. Boundary diffs match exactly
and contain only authorized changes. Eight installed resource instances match
frozen Git bytes and before/after inventories. All captured commands are scoped,
no patch rejection or model-error/invalid-JSON flags. Boundary skill's successful
patches under canonical paths are a runtime observation, not a controlled proof
that prior unknown-target rejections were caused or fixed by path aliases.
No author replay or extra model session was performed.

Do not rerun these cases for a favorable aggregate. Keep Friday's narrow favorable
token observation with its unequal coverage and timing limits. Receipt's next
execution improvement needs lossless status collection, not weaker verification,
another blanket instruction to run fewer commands, or a universal new harness.
Con Artist was deliberately not rerun: its fast single-audit path cannot exercise
the changed batch-output references. The full objective remains unmet.
