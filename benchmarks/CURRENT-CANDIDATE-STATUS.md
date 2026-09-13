# Current candidate: performance objective remains unmet

The goal is better developer outcomes at similar or lower token/time cost across
all eight hires. Current evidence does **not** establish that goal. Passing tests,
shorter instructions and helper-only savings are not whole-task performance wins.

This is a current summary. The [development record](CANDIDATE-DEVELOPMENT-LOG.md)
preserves the previous page in full, including adverse results and historical
test counts. “Current” and “latest” in that archive refer to the original entries.

## Latest evidence

- Con Artist [line-based context selection](../skills/con-artist/references/python-context.md)
  resolves traceback-style `file.py:123` directly to the smallest enclosing
  Python definition without importing project code. Behavioral tests cover
  decorators, nested/conditional definitions, invalid/module-level lines and
  CLI failure without partial output. An author CLI exercise on HTTPX resolves
  `_models.py:252` to `Headers.get_list`; 315 local tests pass. This is navigation
  functionality, not measured model adoption or token/time savings. Featured
  benchmark numbers are unchanged.

- [Committed source-archive gate](../docs/RELEASE-READINESS.md): unmodified
  `c2fd79e` passes local Linux/Python 3.12 validation and 310 tests, with two
  explicit Git-provenance skips (312 discovered). A separate archive CI job
  preserves the checkout matrix; its actual Bash script is tested for committed
  rather than dirty input and failure propagation. Hosted execution and model
  efficiency remain unproven; no account restriction was bypassed.

- [Linux distribution check](../docs/RELEASE-READINESS.md): the `10d416f` source
  archive exposed three Python 3.12 test-portability failures. With the three
  test corrections, 309 tests pass and two Git-provenance checks explicitly skip
  (311 discovered); original model fixtures are unchanged. Local Linux arm64,
  network disabled, existing pure-Python PyYAML mounted read-only. Hosted run
  34741549262 never started steps due to GitHub's payment/spending-limit gate;
  local success does not resolve it or prove model efficiency.

- Receipt final-check example candidate: the entrypoint now gives an adaptable
  native shell chain for actual tests, scoped whitespace check and scoped diff,
  rather than only asking for batching. Its code block is extracted and executed
  in a real temporary Git project: a real assertion failure stops the chain;
  passing tests with trailing whitespace stop before the diff; a clean fix
  executes all checks with the current regression unchanged. Untracked files
  require separate review and all-run requirements still require separate exit
  capture. This demonstrates shell behavior, not model adoption or cost savings.

- [Receipt current-bug regression](results/receipt-current-bug-01/README.md):
  consolidated `7e1e1db` retains actual before failure and unchanged after pass;
  baseline has after-only evidence. Identical final diffs, but +34.16% tokens /
  +6.48% time and unbatched discovery/final checks. Unequal verification and one
  exposed tiny task prevent causal claims; the efficiency objective remains unmet.

- Earlier Receipt entrypoint consolidation: 356 → 289 whitespace-delimited
  words, retaining the explicit scope boundary, historical routing, unchanged
  before/after assertions, qualified suite reuse, separate exit statuses and
  authorization limits. No new helper/reference lookup was added. Existing
  `inspect_usage.py`/`inspect_output_reuse.py` on invoice baseline/skill/scope
  recheck yield respectively 8,725/12,726/13,564 captured command-output
  characters and zero exact recurring long-line characters (default threshold
  80). The skill/reference read commands alone return 6,014/6,359 characters
  including Git output. This motivates reducing shared instructions, but neither
  character counts nor word reduction attributes model tokens or proves savings.
  Current-bug behavior and costs are measured above, without an efficiency win;
  historical-mode effects remain unmeasured. Existing invoice/scope results
  belong to their frozen predecessors.

- [Friday input-budget correction](FRIDAY-INPUT-BUDGET-01.md): rejects known
  combined overflow before opening another file and bounds each read against
  post-stat growth. A 100-selection oversized recipe reads twice instead of
  100 times; the same behavior test fails against the previous implementation.
  Exact-limit SQL and CRLF execution pass; 310 local tests pass. This is author
  input-preparation evidence, not model-token or whole-task performance evidence.

- Receipt CLI usability candidate: `compare.py --help` now includes a complete
  stdin JSON recipe, field meanings, option defaults/limits and the distinction
  between collected observations and proof. A subprocess test extracts the
  printed recipe and executes it against real Git history: the current assertion
  fails before and passes after, originals remain unchanged, and copies are
  cleaned. This addresses the previously uninformative help lookup, not its
  frequency: help output is larger, the normal skill entrypoint is unchanged,
  and whole-task cost/adoption effects are unmeasured. No benchmark score change.

- [Receipt scope recheck](results/receipt-scope-recheck-01/README.md): `b7ae490`
  keeps supplied instructions and further discovery inside authorized roots.
  One skill-only session stays project-local and retains both failures, both
  controls and all four after passes. 130,608 tokens / 53.747 seconds, no baseline
  comparison. A wrong fixture path, repeat discovery and extra helper-help call
  remain; one scope pass is not broad reliability or efficiency evidence.

- [Receipt nested-invoice transfer](results/receipt-invoice-01/README.md):
  helper/directory use retains both defect failures and both controls, but
  +30.08% tokens and a skill-side parent/ancestor instruction-search scope
  failure. Recorded −21.19% time is confounded by concurrent author regression
  tests during baseline and unequal probes. No accepted speedup or scope pass.

- Receipt follow-up candidate: the historical-comparison
  [reference](../skills/receipt/references/existing-fix.md) now directs discovery
  from the located regression/fix and their imports/input references, narrowing
  further listings to unresolved paths. Applicable instructions, configuration
  and cooperating code still require inspection; directory selection is not
  evidence of input completeness. Existing helper constraints are condensed,
  not removed, keeping reference length essentially unchanged. This addresses
  the repeated inventory observed below; behavioral adoption and cost effects
  of the new guidance are now measured in the invoice transfer above: necessary
  inputs retained, but higher tokens and a scope failure. No executable helper
  change and no accepted performance improvement.

- [Receipt directory model adoption](results/receipt-directory-model-01/README.md):
  the model selects `samples/` and uses the helper without reading its source;
  both original defects fail before and pass after. Recorded +3.03% tokens /
  −32.50% time. Repository-wide file enumeration persists; baseline duplicates
  suite execution and searches its parent directory. One exposed pair, unequal
  work and a baseline scope exception prevent an accepted broad efficiency win.

- [Receipt support-directory candidate](RECEIPT-DIRECTORIES-01.md): `0d5c81c`
  freezes explicit current test/support directories across two historical
  implementations, with leaf hashes, overlap rejection and bounded traversal.
  Real temporary-Git/CLI checks reproduce the intended failure then pass with
  unchanged inputs. Integration replay on the existing record-parser and
  multi-module assembly fixtures additionally verifies leaf/directory recipe
  equivalence: identical revisions, input hashes and required failure/pass
  outcomes. Subsequent model adoption and costs are reported above; directory
  use alone does not establish a performance improvement.

- [Two-boundary header transfer](results/httpx-headers-01/README.md): automatic
  index/body readback and batch reuse observed in a new function area. +35.1%
  tokens / −14.9% time; both arms reuse correct suite/control results, baseline
  adds separate import processes and a path repair. Required core outcomes
  present; unequal work and one authored pair do not establish broad savings.

- [Qualified context recheck](results/httpx-context-02/README.md): `3ff951f`
  selects the exact method; +3.2% tokens / −7.0% time, required core outcomes
  present, unequal provenance and baseline scope exception. Automatic large-file
  indexes are author-tested but unused in this cell. 296 local tests pass;
  subsequent `a2b6258` clarifies index limitations. Broad efficiency remains unmet.

- [Context collector model recheck](results/httpx-context-01/README.md): adopted
  once, no repeated instruction search; +47.1% tokens / −23.9% time. Required
  fault/normal outcomes present, but full implementation-file output and helper
  inspection remain costly. One exposed pair, unequal provenance; token objective
  unmet and broad savings unproven.

- [Read-only context candidate](CON-ARTIST-CONTEXT-01.md): `d442b3b` collects
  selected Python source, ancestor instructions/configuration and conftest indexes
  without importing project code. Actual HTTPX CLI exercise and ten new behavior
  tests pass. Subsequent model adoption is reported above; whole-task token
  savings remain unproven.

- [Query parameter transfer](results/httpx-queryparams-01/README.md): entrypoint
  `613d2ee` prioritizes assertion-local discovery and reuse; the actual skill
  session still repeats searches. +17.7% tokens / −12.8% time, required core
  outcomes present; baseline scope exception and unequal provenance checks.
  Discovery-work reduction and broad savings are not demonstrated.

- [Native probe model recheck](results/httpx-decoder-03/README.md): `89d91af`
  selected successfully without repair; +16.5% tokens / −30.4% time across two
  exposed HTTPX tasks. UTF-8 alone −1.0% tokens / −28.6% time, with extra Trio and
  caller-binding checks. Core conclusions correct; unequal work, n=1 and higher
  aggregate tokens prevent broad efficiency acceptance. No featured chart change.

- [HTTPX routing recheck](results/httpx-decoder-02/README.md): helper adopted in
  both skill cells; +32.0% tokens / −15.1% time against fresh baselines. Core
  conclusions correct, work unequal, token objective unmet. Follow-up `89d91af`
  adds native probe files to avoid nested source-string construction; actual
  HTTPX witness replay and 280 local tests pass. Its subsequent model recheck is
  reported above; neither run replaces the other's observations.

- [External HTTPX decoder transfer](results/httpx-decoder-01/README.md): both arms
  reach correct scoped conclusions on real upstream code, but skill +53.8% tokens /
  +14.4% process time. The subsequent `22389f3` routes compatible copy-based audits
  to the existing helper; the recheck above now measures that routing. No new
  result replaces this adverse comparison.

- [Native project integration, four sessions](results/mother-native-project-01/README.md):
  both arms reuse native unittest support on an incompatible helper interface,
  preserve originals and reproduce actual defects. Raw skill costs −21.6% tokens /
  −21.7% time, but unequal coverage, a support-code naming defect and an invalid
  clean-control premise prevent a clean comparative win. No false-positive score.

- [Success-state correction](MOTHER-SUCCESS-STATE-03.md): `b7058c6` fixes three
  demonstrated false-pass paths without adding sequences; retains transient
  failure states and clarifies compatible interfaces. 270 local tests pass.
  Current model cost and real-project routing remain unmeasured; earlier recovery
  percentages refer to the prior revision, not this change.

- [Recovery and retained evidence, 8 sessions](results/mother-recovery-02/README.md):
  `699cdba` catches an error-recovery defect the prior helper missed and retains
  same-run JSON. Both arms meet required outcomes 4/4; skill −17.2% total tokens /
  −67.0% process time. Two closely related authored development cases, two repeats;
  baseline performs additional overlap checks. Not identical-work or broad savings.

- [Mother-in-law browser evidence deduplication](MOTHER-BROWSER-DEDUPE-01.md):
  browser coverage remains 3/3 while tokens fall 18.1% from the prior skill cell;
  the same-snapshot five-case check is only -11.8% tokens / -31.6% time, so the
  favorable browser cell is not mixed into the published checkpoint.

- [Browser model screen](BROWSER-MODEL-01-REVIEW.md): both browser launches abort;
  no browser interaction verified. Skill +34.17% tokens / −1.55% time with extra
  handler-only fallback work; baseline has a project-scope exception. Not a win.

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
The optional helpers are not mandatory for every task.

| Skill | Current entrypoint; supporting resources | Most relevant evidence | Remaining gap |
| --- | --- | --- | --- |
| Necromancer | `51ce19e`; collector `6318b91`, reference `3157ee2` | [Scoped discovery](NECROMANCER-DISCOVERY-01.md), [adverse packaging transfer](NECROMANCER-PACKAGING-REVIEW-01.md), [decision gate](NECROMANCER-DECISION-GATE-01.md) | Configured consumer preserved with near-identical cost; favorable packaging discovery pair has unequal work and capture limits; earlier transfer adverse; broad savings unproven |
| Receipt | [Entrypoint with native final-check example](../skills/receipt/SKILL.md); helper help `0939e0c` | [Current-bug regression](results/receipt-current-bug-01/README.md), [scope recheck](results/receipt-scope-recheck-01/README.md), [invoice transfer](results/receipt-invoice-01/README.md) | Prior current-bug +34.16% tokens with fuller before evidence than baseline; new example author-tested, model effects unmeasured; broad efficiency unresolved |
| Landlord | `26a310d` | [Application-first discovery](LANDLORD-SOURCE-SCOPE-01.md), [compact regression](LANDLORD-COMPACT-01.md), [HTTPX auth design](HTTPX-AUTH-DESIGN-01.md) | Caller search excludes installed example content but still lists resource paths; 68,509 tokens/39.233s in nonpaired regression, no causal efficiency claim; earlier comparisons adverse |
| Mother-in-law | `b7058c6`; success-state/evidence helper | [Native project integration](results/mother-native-project-01/README.md), [false-pass correction](MOTHER-SUCCESS-STATE-03.md), [prior recovery screen](results/mother-recovery-02/README.md) | Native-runner reuse verified on one authored project shape with two variants; raw lower costs have unequal coverage and fixture defects; external-project utility and broad efficiency unproven |
| Exorcist | `ca2e179`; helper/reference `cb10067` | [Signal transfer](EXORCIST-SIGNAL-01.md), [required provenance](EXORCIST-PROVENANCE-01.md) | Signal sum -3.9% tokens / -7.0% time, confounded by baseline repair and unequal work; normal path still costlier in tokens and output routing mixed |
| Hostage Negotiator | `6c5e452` | [Real packaging repair](PACKAGING-REPAIR-01.md), [compact regression](HOSTAGE-COMPACT-01.md), [command transfer](HOSTAGE-COMMAND-01.md) | Packaging pair -11.8% tokens / -6.6% time with unequal coverage and test repairs; other tasks adverse; broad efficiency unproven |
| Con Artist | entrypoint/indexed context `3ff951f`, limitation `a2b6258`; native probes `89d91af` | [Header transfer](results/httpx-headers-01/README.md), [qualified context](results/httpx-context-02/README.md) | Index/body readback and batch reuse observed; header tokens +35.1% / time −14.9% with unequal work; broad savings unproven |
| Friday | entrypoint `9cae27c`; bounded-input helper/reference `fc2c205` | [Input budget](FRIDAY-INPUT-BUDGET-01.md), [Changed paths 03](CHANGED-PATHS-03.md), [interior branch](FRIDAY-BRANCH-01.md) | Input overflow rejected before wasteful reads; SQL-budget checks/migration chunks verified; rolling-schema pair favorable but branch transfer costlier; broad efficiency unproven |

## Reproducibility and release status

- Full local checkout regression at `254e703`: 240 tests pass in 38.612 seconds
  on macOS/Python 3.9.6. Both exported nested-interaction projects replay in
  separate temporary directories without private logs or Git. This is not a
  current archive, hosted-CI or model-efficiency result.

- [Source archive](../docs/RELEASE-READINESS.md), snapshot `a61fec7`: 243 tests
  discovered without Git history/private logs/browser dependencies; 241 execute
  and pass, two pinned-history comparisons skip (36.940 seconds). Browser staging
  mechanics use synthetic dependencies; this does not execute model browser QA.
- [Try the executable example](../examples/con-artist.md) without model usage.
  It demonstrates missed faults and stronger assertions, not model superiority.
- [Inspectable Landlord comparison](results/landlord-compact-01/README.md):
  commands, outputs, answers and usage, including its adverse result.
- [Host installation evidence](../docs/INSTALLATION-TEST.md) is historical.
  Current package execution tests do not prove current host or remote installation.
- The repository remains a private development preview. Hosted CI at `10d416f`
  was checked and is blocked before execution by GitHub's account restriction;
  publication remains unverified. See [release gates](../docs/RELEASE-READINESS.md).
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
