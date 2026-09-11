# Current candidate: performance objective remains unmet

The goal is better developer outcomes at similar or lower token/time cost across
all eight hires. Current evidence does **not** establish that goal. Passing tests,
shorter instructions and helper-only savings are not whole-task performance wins.

This is a current summary. The [development record](CANDIDATE-DEVELOPMENT-LOG.md)
preserves the previous page in full, including adverse results and historical
test counts. “Current” and “latest” in that archive refer to the original entries.

## Latest evidence

- [Nested discovery screen](INTERACTION-NESTED-01-REVIEW.md): required nested
  instructions and tests followed, skill −16.68% tokens / −11.46% time; additional
  sequence coverage differs. One exposed pair is not broad efficiency evidence.

- [Interaction runner reuse candidate](INTERACTION-RUNNER-REUSE-CANDIDATE.md):
  Mother-in-law now prefers an existing sufficient runner deadline over a
  redundant self-spawning wrapper. [One-task screen](INTERACTION-RUNNER-01-REVIEW.md)
  observes reuse by both arms: −13.21% skill tokens / +22.57% time. Not a broad win.

- [Current nine-task combined gate](BUNDLE-CURRENT-02-REVIEW.md): all 18 sessions
  finished and reviewed; **+10.33% total tokens / +23.08% summed process time**.
  Missing before evidence, a scope exception, an omitted history criterion and
  missing QA output remain in accounting. Eight of nine skill cells use more
  tokens and eight take longer. Current broad efficiency is not accepted.

- [Automatic two-fault audit](PROBE-ADOPTION-01.md): Con Artist selected, helper
  unused; **+24.92% tokens / −5.97% time**. Native harnesses already shared the
  correct stronger-test observation. Unequal work and partial output prefixes
  limit comparison. New same-process provenance guidance has no model result.
- [Local helper comparison](CON-ARTIST-PROBE-REUSE-01.md): identical probes use six
  child checks instead of seven, averaging about 38 ms less. Different probes
  correctly keep seven. This is not a model-token or whole-task result.
- [Automatic Store/Receipt comparison](CURRENT-SELECTION-01.md): both use more
  tokens than baseline; time is mixed. Work differs and broad search incidentally
  reads another skill's example. Current all-eight recall is not established.
- [Configured Landlord consumer](LANDLORD-CONFIGURED-01.md): relevant code under
  examples is followed and exercised. One unpaired sample is not an efficiency win.
- [Original 72-session comparison](REPORT-2026-09-11.md): historical, not current
  resources. It did not establish resource savings; its graphs remain unchanged.

## Current resources and gaps

Revisions identify each group's last change, not necessarily the snapshot used by
its linked experiment. Character identities and automatic selection remain intact.
The five optional helpers are not mandatory for every task.

| Skill | Current entrypoint; supporting resources | Most relevant evidence | Remaining gap |
| --- | --- | --- | --- |
| Necromancer | `51ce19e`; collector `6318b91`, reference `3157ee2` | [Scoped discovery](NECROMANCER-DISCOVERY-01.md), [adverse packaging transfer](NECROMANCER-PACKAGING-REVIEW-01.md), [decision gate](NECROMANCER-DECISION-GATE-01.md) | Configured consumer preserved with near-identical cost; favorable packaging discovery pair has unequal work and capture limits; earlier transfer adverse; broad savings unproven |
| Receipt | `abb4b93`; helper/reference `4a29990` | [Two-module transfer](RECEIPT-ASSEMBLY-01.md), [equal explicit requirements](RECEIPT-EQUAL-REQUIREMENTS-01.md), [earlier adverse package](RECEIPT-CURRENT-PACKAGE-01.md) | Two-module transfer +26.0% tokens / −31.1% time despite correct before/after checks; earlier parser pair favorable; combined efficiency unmet |
| Landlord | `26a310d` | [Application-first discovery](LANDLORD-SOURCE-SCOPE-01.md), [compact regression](LANDLORD-COMPACT-01.md), [HTTPX auth design](HTTPX-AUTH-DESIGN-01.md) | Caller search excludes installed example content but still lists resource paths; 68,509 tokens/39.233s in nonpaired regression, no causal efficiency claim; earlier comparisons adverse |
| Mother-in-law | `8b81a59` | [Discovery candidate](INTERACTION-DISCOVERY-CANDIDATE.md), [runner adoption](INTERACTION-RUNNER-01-REVIEW.md), [protected path](CONDITIONAL-PATHS-01.md) | Discovery revision unmeasured; prior runner screen −13.21% tokens / +22.57% time with direct failure output; older captures partly missing; browser/recovery coverage limited |
| Exorcist | `ca2e179`; helper/reference `cb10067` | [Signal transfer](EXORCIST-SIGNAL-01.md), [required provenance](EXORCIST-PROVENANCE-01.md) | Signal sum -3.9% tokens / -7.0% time, confounded by baseline repair and unequal work; normal path still costlier in tokens and output routing mixed |
| Hostage Negotiator | `6c5e452` | [Real packaging repair](PACKAGING-REPAIR-01.md), [compact regression](HOSTAGE-COMPACT-01.md), [command transfer](HOSTAGE-COMMAND-01.md) | Packaging pair -11.8% tokens / -6.6% time with unequal coverage and test repairs; other tasks adverse; broad efficiency unproven |
| Con Artist | `8b61ed8`; helper/common/advanced references `91fdde3` | [Automatic audit and subsequent candidate](PROBE-ADOPTION-01.md), [report interpretation](CON-ARTIST-REPORT-01.md), [counter regression](HTTPX-COUNTER-01.md) | Auto audit +24.92% tokens / −5.97% time; helper unused. Same-process provenance instruction is newer and has no model result |
| Friday | `9cae27c`; helper `64dd877`, reference `ea48fde` | [Changed paths 03](CHANGED-PATHS-03.md), [interior branch](FRIDAY-BRANCH-01.md) | SQL-budget fail-fast regressions verified for checks and migration chunks; rolling-schema pair favorable but branch transfer costlier; broad efficiency unproven |

## Reproducibility and release status

- [Source archive](../docs/RELEASE-READINESS.md), snapshot `05a9fce`: 235 tests
  discovered without Git history/private logs; 233 execute/pass, two pinned
  history comparisons skip (35.925 seconds). The current two-fault example also
  executes separately from that extraction.
- [Try the executable example](../examples/con-artist.md) without model usage.
  It demonstrates missed faults and stronger assertions, not model superiority.
- [Inspectable Landlord comparison](results/landlord-compact-01/README.md):
  commands, outputs, answers and usage, including its adverse result.
- [Host installation evidence](../docs/INSTALLATION-TEST.md) is historical.
  Current package execution tests do not prove current host or remote installation.
- The repository remains a private development preview. Current hosted CI and
  publication are unverified; see [release gates](../docs/RELEASE-READINESS.md).
  Visibility, billing and publication changes require owner authorization.

## Interpretation and integrity

Total tokens include cached input plus output once; missing usage is not zero.
Completion, test counts and exit codes do not alone establish correct behavior.
Review actual assertions, outputs, scope and resource identities.

Clear capture diagnostics can coexist with partial output. Missing original
output is not reconstructed from final prose or credited author replay. Unequal
verification depth, failed patches, run order and shared caches remain limitations.
Reused observations are not independent executions. Retain failures and adverse
samples; do not rerun exposed tasks or change criteria to seek favorable scores.

## Remaining acceptance work

1. Remove demonstrated end-to-end developer work on representative repository
   tasks while preserving required outcomes and the character concept. Helper
   microbenchmarks and shorter wording alone do not satisfy this.
2. Compare with a contemporary baseline at equivalent requested outcomes. Keep
   development batches below ten tasks and freeze criteria/versions beforehand.
   The existing nine-case set is for regression, not score optimization.
3. Verify a separate confirmation set and a current combined all-eight gate.
   Broad efficiency and the requested substantial improvement remain unproven.
4. Complete installation and release gates for the intended revision, with owner
   authorization. Local checks cannot substitute for hosted CI or publication approval.

Prior steps remain in the [development record](CANDIDATE-DEVELOPMENT-LOG.md) and
linked individual reports. No numerical definition of “huge” has been agreed;
do not substitute reliability alone or a smaller easy task for the full goal.
