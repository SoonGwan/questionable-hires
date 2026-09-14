<p align="center"><img src="assets/team.svg" alt="Questionable Hires — Weird, but employed. Unfortunately, essential." width="100%"></p>

<p align="center"><img src="assets/team-characters.png" alt="Eight Questionable Hires as tiny, deadpan doodle characters." width="100%"></p>

<p align="center"><a href="docs/INSTALL.md">Hire the team</a> · <a href="examples/README.md">See them work</a> · <a href="benchmarks/CURRENT-CANDIDATE-STATUS.md">Read the evidence</a> · <a href="README.ko.md">한국어</a></p>

# Questionable Hires

Eight suspiciously effective engineering coworkers for your AI agent.

One demands receipts. One charges your abstractions rent. One talks to developers who left in 2019. Hiring was a mistake. Firing them would be worse.

Each character carries one engineering habit: trace the reason, prove the fix, test the awkward sequence, or keep the release reversible. Built with GPT-6 Astra in mind, using portable skill files.

**Development preview.** All eight hires have been exercised on small synthetic tasks. The baseline usually reached the same central answer. We show actual comparisons and limitations rather than claim a universal improvement.

## The test passed. The record disappeared.

This test looks reassuring:

```python
self.assertTrue(save([], 'record')['ok'])
```

Ask `$con-artist` whether it catches a lost write. In an actual run, it removed the write in a disposable copy:

| Check | Real write | Write removed |
| --- | --- | --- |
| Existing `ok` assertion | Pass | Pass |
| Assertion on stored record | Pass | Fail |

The smallest useful improvement:

```python
store = []
self.assertTrue(save(store, 'record')['ok'])
self.assertEqual(store, ['record'])
```

Production code stayed intact. The no-skill baseline also found this flaw. [Compare all three runs →](examples/con-artist.md)

## Meet the team

| Hire | Unfortunate personality | Useful engineering instinct |
| --- | --- | --- |
| [Necromancer](examples/necromancer.md) | “Their reasons didn't leave with them.” | Trace legacy behavior through callers and history. |
| [Receipt](examples/receipt.md) | “You fixed it? Show me the receipt.” | Verify a fix with a real before/after reproduction. |
| [Landlord](examples/landlord.md) | “Who's paying rent on this abstraction?” | Make abstractions earn their maintenance cost. |
| [Mother-in-law](examples/mother-in-law.md) | “And if I click it twice?” | Reproduce realistic interaction and timing failures. |
| [Exorcist](examples/exorcist.md) | “Let's test your belief in the cache.” | Distinguish debugging hypotheses with experiments. |
| [Hostage Negotiator](examples/hostage-negotiator.md) | “Release the button. The architecture stays.” | Deliver focused changes without optional scope creep. |
| [Con Artist](examples/con-artist.md) | “Your mock is impressed with itself.” | Find tests that let broken behavior pass. |
| [Friday](examples/friday.md) | “Can Monday-you undo this?” | Review version compatibility and recovery paths. |

## Hire one. Or make eight questionable decisions.

With Node.js/npm and Git, install one hire or the whole team:

```sh
npx skills add SoonGwan/questionable-hires
```

Tested with `skills@1.5.26` (Node.js 22.20.0+): [all-eight local installation check](benchmarks/SKILLS-CLI-INSTALL-01.md). Remote authentication/public installation is not covered by that check.

The installer discovers all eight hires and lets you select skills and supported
agents. For one project-local Codex skill without prompts:

```sh
npx skills add SoonGwan/questionable-hires --agent codex --skill mother-in-law --copy -y
```

This uses the independent [`skills`](https://github.com/vercel-labs/skills) CLI;
review it and the selected skills before execution. During the private preview,
Git credentials are required. After the repository is public, the same command
works without repository access.

Or use the bundled Python 3.8+ installer directly:

```sh
git clone https://github.com/SoonGwan/questionable-hires.git
cd questionable-hires
python3 scripts/install.py --dest /path/to/your-project/.agents/skills --skill necromancer
```

Replace the project path. Omit `--skill necromancer` to install all eight; add `--dry-run` to preview. Existing skill folders are never overwritten.

Already installed? Use `--check` instead of `--dry-run` to compare installed bytes
and file modes with this checkout. It reports missing/changed/extra resources
without writing; exit 0 means matching, 2 differences, 1 comparison failure.
It does not update copies or establish that this checkout is the remote latest.

Install from a trusted checkout: linked source files or directories are rejected
before writing. On failure or cancellation, the installer attempts to remove
only folders it created. Cleanup can fail too, so inspect any remaining partial
folders before retrying; preserve existing files and personal edits.

In a new Codex CLI or IDE thread:

```text
$necromancer Can we remove this workaround?
$receipt Verify that this fix actually prevents duplicate submissions.
$friday Review this release's rollout and rollback plan.
```

Normal automatic selection is enabled. No lifecycle hooks, telemetry, background services, or model-setting changes. [Installation, updates, and removal →](docs/INSTALL.md)

### Some coworkers brought tools

Start with a normal skill request; helpers are optional when the project lacks
equivalent support. The Python helpers require **Python 3.9+**; Con Artist's
mutation runner, Receipt and Exorcist also require POSIX. Hostage's standalone
JavaScript module needs a JavaScript runtime, **not Python**; its native tests
use Node.js. Helpers do not install dependencies or run in the background.

| Hire | Optional support / boundary |
| --- | --- |
| Hostage Negotiator | Controlled [Python calls](skills/hostage-negotiator/assets/controlled_call.py) or [JavaScript calls and cleanup](skills/hostage-negotiator/assets/controlled_call.mjs). Tests still own application assertions; no browser evidence. |
| Con Artist | [Disposable Python test audits](skills/con-artist/references/python-audit.md) and [read-only context collection](skills/con-artist/references/python-context.md). Run trusted tests only; not a sandbox. |
| Necromancer | [Focused Git history](skills/necromancer/references/focused-history.md). Attribution is evidence, not a decision to keep or delete code. |
| Friday | [SQLite compatibility checks](skills/friday/references/sqlite-matrix.md). Not proof of production rollout safety or other DB engines. |
| Receipt | [Before/after Python fix verification](skills/receipt/references/existing-fix.md). Preserve the reproduction, source identity and both results. |
| Exorcist | [Bounded foreground probes](skills/exorcist/references/bounded-probe.md). Not for background services. |
| Mother-in-law | [Controlled interaction checks](skills/mother-in-law/SKILL.md) for compatible UI-less Python components. Existing project tests take precedence; not browser verification. |
| Landlord | [Review guidance](skills/landlord/SKILL.md); no separate bundled runtime helper. |

**Evidence is mixed.** Some tools are demonstrably useful, but installing them
does not establish lower model cost. The state-content correction catches
a previously missed fault; broad all-eight efficiency remains unproven.
[Current reviewed status](benchmarks/CURRENT-CANDIDATE-STATUS.md).

<details>
<summary>Per-tool development results, adverse runs and known limitations</summary>

[Landlord and Hostage discovery routing](benchmarks/DISCOVERY-ROUTING-01-REVIEW.md)
does not demonstrate savings: atomic skill costs more and Store skill times out
after a connection error. All attempts and missing usage are retained.

- **Hostage Negotiator:** optional [controlled asyncio callbacks](skills/hostage-negotiator/references/async-callback.md) replace repeated entry/release gates when project support is absent. Tests retain application assertions and task cleanup. [Model adoption](benchmarks/HOSTAGE-CALL-MODEL-01-REVIEW.md) is observed, but baseline timeout and absent original test output prevent an accepted efficiency comparison. Separate native replay passes the implementation and rejects defect controls; it does not fill the original evidence gap.
  A [copy-check model screen](benchmarks/HOSTAGE-COPY-CHECK-MODEL-01-REVIEW.md) adopts byte comparison but still reads the full implementation. Original 43/43 tests and 12 separate replay controls pass their expected outcomes; no efficiency win is established.
  Optional [task-aware entry waits](benchmarks/HOSTAGE-ENTRY-WAIT-MODEL-01-REVIEW.md) are adopted in fresh model tests: final 45/45 passes, with eight skipped-callback defects detected in about 0.10s during separate replay. The first test transcript is missing; no overall model-efficiency claim.
  A [Python task-aware wait](benchmarks/HOSTAGE-PYTHON-ENTRY-WAIT-01.md) is available too. [Python adoption 01](benchmarks/HOSTAGE-PYTHON-ENTRY-MODEL-01-REVIEW.md) finds an overconstrained duplicate-return assertion and no efficiency win. After the guidance correction, [keyed import 01](benchmarks/HOSTAGE-KEYED-IMPORT-01-REVIEW.md) accepts a valid alternate return and detects ownership/cleanup faults, but has secondary test-diagnostic errors and no efficiency claim (118,971 tokens / 103.161s). Explicit task clarification prevents isolating the skill's effect.
  [Dependent-phase guidance](benchmarks/HOSTAGE-DEPENDENT-PHASES-01.md) and [final-check batching](benchmarks/HOSTAGE-FINAL-BATCH-01.md) are adopted in [final batching model 01](benchmarks/HOSTAGE-FINAL-BATCH-MODEL-01-REVIEW.md): 95,992 tokens / 94.261s, four shell calls, clean separate fault diagnostics. The original ten-test summary lacks five full headers. Descriptive −19.31% tokens / −8.63% time versus keyed-import 01 is not a causal gain (single sessions, unequal verification, shared cache and capture gap).
  Optional [JavaScript Promise callbacks](skills/hostage-negotiator/assets/controlled_call.mjs) provide standalone ES-module support too. [Native validation](benchmarks/HOSTAGE-JAVASCRIPT-CALL-01.md) covers identity and defect controls. A [model screen](benchmarks/HOSTAGE-JAVASCRIPT-PANEL-01-REVIEW.md) confirms adoption and passing regressions, but costs **93.51% more tokens and 11.32% more time** than baseline on one authored task. No efficiency or browser-coverage claim.
  The current module also offers an optional [bounded lifecycle wrapper](benchmarks/HOSTAGE-JAVASCRIPT-SCOPE-01.md) for registered tasks and callback cleanup. A [fresh development pair](benchmarks/HOSTAGE-JAVASCRIPT-SCOPE-MODEL-01-REVIEW.md) uses it and preserves regression coverage: **10.80% more total tokens, 6.70% less time**; less authored test code but more code including copied support. Not a general efficiency claim. The preceding screen predates this wrapper.
  A subsequent [usage-first screen](benchmarks/HOSTAGE-JAVASCRIPT-USAGE-MODEL-01-REVIEW.md) confirms shorter reads with unchanged runtime code, but still costs **30.82% more tokens / 6.75% less time** in its fresh exposed-task pair. No overall efficiency win is established.
  A [two-stage preview transfer](benchmarks/HOSTAGE-JAVASCRIPT-PREVIEW-01-REVIEW.md) observes **14.22% more tokens / 31.46% less time**, but a post-review fault escapes all 54 skill tests while baseline detects it. Faster timing is not an accepted overall gain; state-content regression protection needs improvement.
  [Fresh state-content adoption](benchmarks/HOSTAGE-STATE-CONTENTS-MODEL-01-REVIEW.md) now detects that blind spot in model-generated tests and accepts correct mutable updates. This skill-only run costs 171,403 tokens / 130.943s; it is behavioral evidence, not a new efficiency comparison.
  New [verification-delivery guidance](benchmarks/HOSTAGE-VERIFICATION-DELIVERY-01.md) separates test results from a final shell status; its isolated causal effect is unmeasured. The collector flags missing summaries for review, not automatic scoring.
  A [keyed-publication transfer screen](benchmarks/HOSTAGE-KEYED-PUBLISH-01-REVIEW.md) confirms asset reuse and standalone test status, but +25.25% tokens / +7.64% time and partial original logs prevent an efficiency claim. Separate unchanged-test controls support correctness without replacing missing output.
  The latest [single-read interface](benchmarks/HOSTAGE-SINGLE-READ-01.md) is [adopted in a fresh screen](benchmarks/HOSTAGE-SINGLE-READ-MODEL-01-REVIEW.md) with required transitions retained: +6.42% tokens / −7.50% time. Grouped tests, unequal extra checks and partial native headers limit interpretation; this is not a general efficiency win.
- **Con Artist:** disposable Python mutation audits with copied-import checks, separate test/probe exit statuses, bounded log memory and timeouts. [Usage and limits](skills/con-artist/references/python-audit.md). Run trusted tests only: this is not a sandbox.
  [Focused native-probe routing](benchmarks/CON-ARTIST-PROBE-ROUTING-01.md) is adopted in the [model screen](benchmarks/CON-ARTIST-PROBE-ROUTING-MODEL-01-REVIEW.md), retaining four native audit phases. It records 96,455 tokens / 46.178s: 3.42% fewer tokens and 6.35% less time than the previous skill session, but still 11.96% more tokens than the earlier baseline. Unequal work, exposed n=1 and shared cache prevent a causal or baseline-superiority claim.
  [SQLite transfer 01](benchmarks/CON-ARTIST-SQLITE-01-REVIEW.md) verifies real disk commits through endpoint aliases and existing native fixtures. Skill captures all four phases but costs 15.92% more tokens / 28.65% less time. Baseline's original positive-control output is missing; separate unchanged-program replay cannot fill it. Adoption is supported, broad efficiency is not.
  The [core-guide candidate 01](benchmarks/CON-ARTIST-CORE-GUIDE-01.md) shortens routine documentation by 27.81% in bytes (core plus advanced: 9.27%). All 88 helper/packaging tests pass. The [subsequent model screen](benchmarks/CON-ARTIST-CORE-GUIDE-MODEL-01-REVIEW.md) captures the four audit phases at 73,679 tokens / 35.540s, but no project-source or guide read is recorded. Guide adoption remains unverified; lower descriptive costs are not an accepted efficiency gain.
  [Foreground-runner cleanup](benchmarks/CON-ARTIST-PIPE-EXIT-01.md) prevents inherited descendant pipes from aborting completed checks; native survival/detection controls pass. Remaining group members are stopped, so background launchers are unsupported. Model-level savings are unmeasured.
  [Checkpoint 06](benchmarks/BUNDLE-CONTRACT-06-REVIEW.md#persistence-audit--skill): actual helper adoption captures all four audit checks. One exposed pair records fewer tokens/time, but baseline repair and incomplete output mean unequal work. Raw/resource reconciliation is complete; pipe-fix savings are not isolated.
  Its optional [read-only context collector](skills/con-artist/references/python-context.md) accepts definition names or traceback-style `file.py:123` selectors and gathers enclosing definitions, ancestor instructions/configuration and conftest indexes without importing project code. Indexes guide inspection; they do not establish test behavior or complete dependency resolution.
  A [physical-line correction](benchmarks/CON-ARTIST-PHYSICAL-LINES-01.md) prevents Unicode separators inside Python strings from silently shifting or truncating excerpts. Native checks cover source integrity; model-level cost impact is unmeasured.
- **Necromancer:** focused current-line attribution and historical patches, including dirty/shallow-history limits. [Usage and limits](skills/necromancer/references/focused-history.md). It collects evidence; it does not decide whether old behavior is still needed.
  A [Git line-boundary correction](benchmarks/NECROMANCER-PHYSICAL-LINES-01.md) preserves embedded Unicode separators and CR content across current text, blame and patch excerpts. Real-Git checks pass; model cost impact is unmeasured.
  A [three-decision development screen](benchmarks/results/necromancer-regions-01/README.md) gets all decisions right in both arms with −15.85% tokens / −18.56% time. Unequal extra verification and one exposed task prevent general efficiency claims; the optional collector was not used.
- **Friday:** reusable in-memory SQLite reader checks across migration and rollback states. [Usage and limits](skills/friday/references/sqlite-matrix.md). Query success is not production readiness; other database engines require their own evidence.
  The [shorter core guide](benchmarks/FRIDAY-CORE-GUIDE-01.md) is used in [short-guide model 01](benchmarks/FRIDAY-CORE-GUIDE-MODEL-01-REVIEW.md): one API execution supplies full column/value assertions, 89,545 tokens / 54.127s. Compared with checkpoint 07, tokens fall 18.13% but time rises 19.88%; unequal work and single sessions prevent a causal efficiency claim.
  [Shared declaration snapshots](benchmarks/FRIDAY-READER-SNAPSHOT-01.md) avoid rereading/parsing one module for several literal queries, while still executing every phase's SQL checks. Local behavior is verified; model-cost impact is unmeasured.
  The latest [result-reuse guidance](benchmarks/FRIDAY-RESULT-REUSE-01.md) makes the existing native Python API available in the core guide. A [fresh screen](benchmarks/FRIDAY-RESULT-REUSE-MODEL-01-REVIEW.md) confirms comparisons from one execution, but +39.28% tokens / +2.04% time and unequal work do not establish efficiency. Runtime remains `e3bc342`.
  [Optional empty phase fields](benchmarks/FRIDAY-PHASE-DEFAULTS-01.md) remove a reproduced API input failure while retaining validation. A [fresh one-task screen](benchmarks/FRIDAY-PHASE-DEFAULTS-MODEL-01-REVIEW.md) confirms first-call adoption, but duplicate SQL execution accompanies +67.14% tokens / +3.12% time. This is a specific usability fix, not proven efficiency.
  A later [two-task interface screen](benchmarks/FRIDAY-INTERFACE-MODEL-01-REVIEW.md) records +68.56% tokens / +8.41% time overall, including an API repair. Conditional guide loading is adopted, but this is not an efficiency win; all attempts remain available.
  [Literal-reader references](benchmarks/FRIDAY-LITERAL-READERS-01.md) read fixed Python query declarations without executing modules or writing a custom extraction loop. Dynamic modules are rejected; static provenance is not proof of runtime binding. A [single-task screen](benchmarks/FRIDAY-LITERAL-MODEL-01-REVIEW.md) confirms adoption with +10.07% tokens / −24.73% time and unequal extra checks—not general savings.
- **Receipt:** frozen current tests and support files against a committed or uncommitted Python fix, including regular `src/` packages without installing them. Records hashes, separate outputs and revision identities. [Usage and limits](skills/receipt/references/existing-fix.md). The [source-layout model check](benchmarks/results/receipt-src-model-01/README.md) adopts the helper with lower recorded costs, but unequal work, a capture gap and one task limit the claim; broad efficiency remains unproven.
  [Native-runner exit cleanup](benchmarks/RECEIPT-PIPE-EXIT-01.md) now prevents an inherited descendant pipe from falsely timing out a finished check and skipping the after comparison. Remaining group members are stopped; background launchers are unsupported. Model-level cost impact is unmeasured.
- **Exorcist:** bounded foreground probe execution with independent process deadlines and bounded captured logs. [Usage and limits](skills/exorcist/references/bounded-probe.md). The [first model check](benchmarks/EXORCIST-PROBE-RUNNER-01.md) uses the helper correctly but does not save resources.
  [Foreground-exit cleanup](benchmarks/EXORCIST-PIPE-EXIT-01.md) now stops remaining group members promptly if they retain the output pipe. It preserves buffered output and direct exit status; background launchers are unsupported. Local checks pass, but model-level savings remain unmeasured.
- **Mother-in-law:** controlled async success, recovery and stale-response checks, with optional same-run JSON evidence. Opt-in display-retention checks cover required normal/reversed overlap. A [three-task development check](benchmarks/results/mother-retention-model-01/README.md) observed adoption with −1.58% tokens / −52.77% time; unequal extra checks and n=1 prevent general claims. A [later delivery-route check](benchmarks/results/mother-routing-01/README.md) increased tokens and exposed a missing intermediate assertion in a generated native test; improvement is not accepted. [Interface and limits](skills/mother-in-law/SKILL.md). For compatible UI-less Python components only; existing project tests take precedence. Its async timeout does not interrupt blocking code or prove browser behavior.

The subsequent [Mother interval-contract check](benchmarks/results/mother-interval-01/README.md) adopts the missing assertion: separate unchanged-test replay rejects the transient fault and accepts a valid correction. Costs still increase **9.32% tokens / 10.58% time**. Two original skill transcripts are partial; replay does not replace them. This is specific coverage progress, not an efficiency win.

The [subsequent work-selection check](benchmarks/results/mother-interval-02/README.md) avoids those extra tests while preserving required assertions in separate replay: **−14.54% recorded tokens / +83.52% time**. Connection resets, one missing original test output and n=1 prevent overall efficiency acceptance; replay does not fill missing model evidence.

</details>

Use the normal skill prompts above; the agent can choose the helper when it saves repeated work. A small task or an already-established result may be cheaper to handle directly. Installing the team does not imply every task should use all eight hires.

## Does it actually work?

<!-- featured-benchmark:start -->

**Latest frozen confirmation:** `mother-in-law` met **5/5** reviewed interaction-QA targets versus baseline **5/5**, with **0** skill false positives. Across 5 new cases committed before execution, the skill used **93.2%** normalized total tokens and **71.3%** normalized elapsed time. This is one fresh session per arm and task, not a whole-team or repeated-sample claim.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="benchmarks/results/mother-in-law-confirmation-2026-09-12/comparison-dark.svg">
  <img src="benchmarks/results/mother-in-law-confirmation-2026-09-12/comparison-light.svg" alt="5-task frozen mother-in-law confirmation: baseline meets 5 of 5 reviewed targets and skill meets 5 of 5; normalized tokens 100 and 93.2 percent; normalized elapsed time 100 and 71.3 percent." width="100%">
</picture>

[Inspect the frozen cases, raw values, method, and limitations](benchmarks/results/mother-in-law-confirmation-2026-09-12/README.md).

<!-- featured-benchmark:end -->

The earlier [candidate-development checkpoint](benchmarks/results/mother-in-law-fast-2026-09-12/README.md)
is retained separately.

**Whole-team checkpoint 08 (2026-09-14): broad efficiency remains unproven.**
The [nine-task review](benchmarks/BUNDLE-CONTRACT-08-REVIEW.md), 18 fresh sessions
at resource snapshot `ecff8a8`, records **0.58% fewer total tokens and 15.08% less
summed process time** with skills. Three task pairs cost more on both axes; six
use more tokens. Unequal extra work and two original test-output gaps remain
disclosed: protected-search baseline and pending-form skill. Twenty-two separate
native controls match expected outcomes; replay does not fill original gaps.
These exposed authored tasks, n=1 per arm and shared host/cache do not prove a
general 20–30% gain or measure later edits. Ratios of sums differ from the original
chart's equal-task means. [Checkpoint 07](benchmarks/BUNDLE-CONTRACT-07-REVIEW.md),
[Checkpoint 05](benchmarks/BUNDLE-CONTRACT-05-REVIEW.md),
[checkpoint 06](benchmarks/BUNDLE-CONTRACT-06-REVIEW.md) and
[earlier adverse results](benchmarks/BUNDLE-CURRENT-02-REVIEW.md) remain preserved.

**The chart below is the original experiment, not a measurement of today's files.** Later candidates have targeted checks, real HTTPX audits/design reviews, and this project's packaging repair recorded in [current candidate status](benchmarks/CURRENT-CANDIDATE-STATUS.md). Results are mixed: local helper gains do not automatically reduce model-session cost, and some comparisons perform unequal verification. Broad performance improvement remains unproven. Historical runs, including [nine-task screen 05](benchmarks/FAST-REGRESSION-05.md), remain available rather than being replaced by a favorable sample.

<details>
<summary>Historical whole-team experiment — 72 sessions on the original skill files</summary>

We completed **72 fresh GPT-6 Astra sessions** at medium reasoning: eight small synthetic tasks × three arms × three repetitions. Baseline = 100%; generic control used **111.9% tokens / 125.1% time**, and the corresponding skill used **111.5% tokens / 117.6% time**. Implementation line churn was identical. Neither arm saved resources in this experiment.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-dark.svg">
  <img src="benchmarks/results/astra-repeat-2026-09-11/analysis/comparison-light.svg" alt="Baseline/control/skill: tokens 100/111.9/111.5%, time 100/125.1/117.6%, implementation LOC 100/100/100%. Strict success 19/24, 16/24, 18/24." width="100%">
</picture>

Strict evidence-and-scope success was **19/24 baseline, 16/24 control, 18/24 skill**. Central fixes and diagnoses generally agreed. Four skill sessions have unresolved rejected-patch records; three control audits changed existing tests. These are unblinded author judgments on tiny synthetic tasks, not proof of superiority or a general safety ranking. No session timed out; no dollar cost is inferred from subscription usage.

[Original repeated experiment, methods and raw evidence](benchmarks/REPORT-2026-09-11.md) · [Reproduce the comparison](benchmarks/README.md) · [Earlier n=1 smoke results](benchmarks/REPORT.md) · [Eight worked examples](examples/README.md)

</details>

Historical whole-team routing checks selected the expected skill files in eight sessions. A historical local bundle also passed CLI installation and removal. See [routing evidence](benchmarks/REPORT.md#automatic-routing-with-the-whole-team) and the dated [installation record](docs/INSTALLATION-TEST.md); these are not checks of every later revision.

Recent evidence, kept separate from the chart:

- [Inspect a recent automatic audit](benchmarks/results/probe-adoption-01/README.md):
  both arms' commands, captured output, answers and usage, including higher token
  cost and no helper adoption. Redactions and missing output are documented.
- [Try a two-fault audit without model usage](examples/con-artist.md#try-the-helper-without-model-usage):
  a runnable helper example, not evidence that the model is faster with the skill.

- [Automatic selection versus no skill](benchmarks/CURRENT-SELECTION-01.md): two appropriate selections, but more tokens in both tasks and mixed elapsed time; actual work differs.
- [Unrelated requests](benchmarks/ROUTING-NEGATIVE-01.md) and [a configured consumer under examples](benchmarks/LANDLORD-CONFIGURED-01.md): narrow routing checks, not general accuracy or efficiency scores.
- [Open a complete previous/candidate comparison](benchmarks/results/landlord-compact-01/README.md): commands, captured outputs, answers and usage you can inspect without private logs. That comparison is adverse too.

These are skill-guided workflows, not guarantees. Actual tool access, model behavior, project complexity, and user instructions determine the outcome. Other hosts and remote marketplace distribution remain unverified.

## Why Astra?

The skills give Astra focused jobs and explicit stopping conditions. User intent takes precedence over the character; routine choices use project context; technical claims need evidence. Humor stays brief. [Design rationale →](docs/ASTRA.md)

## We're unfortunately hiring

A new hire needs a distinct engineering job, a realistic example, and a case where it should leave things alone. Start with [the contribution guide](CONTRIBUTING.md). Use synthetic or public data in reports; see [security reporting](SECURITY.md).

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

[Release readiness and remaining gates](docs/RELEASE-READINESS.md) · [Roadmap](docs/ROADMAP.md) · [Changelog](CHANGELOG.md) · [MIT license](LICENSE)

## Inspiration

[Ponytail](https://github.com/DietrichGebert/ponytail) showed how a memorable character can carry a concrete engineering habit. Our team, skill instructions, and evaluation fixtures are original. We also learned from its published benchmark corrections: use a real agent baseline, isolate the arms, and keep the ties.
