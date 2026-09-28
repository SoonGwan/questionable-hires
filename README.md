<p align="center"><img src="assets/team.svg" alt="Questionable Hires — Weird, but employed. Unfortunately, essential." width="100%"></p>

<p align="center"><img src="assets/team-characters.png" alt="Eight Questionable Hires as tiny, deadpan doodle characters." width="100%"></p>

<p align="center"><a href="https://hires.no-money-do-you-have-money.com/en/">Website</a> · <a href="docs/INSTALL.md">Hire the team</a> · <a href="examples/README.md">See them work</a> · <a href="benchmarks/CURRENT-CANDIDATE-STATUS.md">Read the evidence</a> · <a href="README.ko.md">한국어</a></p>

# Questionable Hires

**Weird, but employed. Unfortunately, essential.**

Eight developer skills for AI coding agents: trace legacy code, prove a fix,
challenge weak tests, or review a release. Each hire has a specific job and stopping
condition. Built with GPT-6 Astra in mind, using portable skill files.

**Development preview. Whole-team quality and cost improvement remain unproven.**
[0.2.0 candidate and release conditions](docs/RELEASE-0.2.0.md) ·
[Choose by the job](docs/CHOOSE-A-HIRE.md) · [Run a demo without model usage](docs/SHARE.md#a-real-demo-without-model-usage)

## Meet the team

Not sure who to ask? [Choose by the job: diagnosis, fix verification, test quality, or review →](docs/CHOOSE-A-HIRE.md)

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

<a id="hire-one-or-make-eight-questionable-decisions"></a>

## Hire one

With Node.js/npm and Git, choose a skill and supported agent:

```sh
npx skills add SoonGwan/questionable-hires
```

For one project-local Codex skill without prompts:

```sh
npx skills add SoonGwan/questionable-hires --agent codex --skill mother-in-law --copy -y
```

These commands use the independent [skills CLI](https://github.com/vercel-labs/skills).
[Installation, updates, removal and the bundled Python installer](docs/INSTALL.md) ·
[Small standalone archive for offline handoffs](docs/STANDALONE-ARCHIVE.md) ·
[Dated public installation verification](docs/PUBLIC-LAUNCH.md).

In a new Codex CLI or IDE thread:

```text
$necromancer Can we remove this workaround?
$receipt Verify that this fix actually prevents duplicate submissions.
$friday Review this release's rollout and rollback plan.
```

<a id="some-coworkers-brought-tools"></a>

Automatic selection is enabled. Installing eight skills does not invoke all eight
on every task. Existing project tests come first; [helper tools and their limits](docs/HELPERS.md)
are optional. No lifecycle hooks, background services, telemetry or model-setting changes.

## Does it actually work?

**Integration07 — 2026-09-28, measured resource `1be35120`: total tokens +1.67%,
CLI elapsed −9.63%; only 2/8 roles reduce both.** Bounded task outcomes were preserved;
quality superiority was not established. These exposed development tasks have one
session per condition, shared host/cache and unequal checks.
[All costs](benchmarks/ALL-EIGHT-CURRENT-07-COSTS.md) ·
[Original review and limitations](benchmarks/ALL-EIGHT-CURRENT-07-REVIEW.md) ·
[Current decision index](benchmarks/CURRENT-CANDIDATE-STATUS.md).

The frozen confirmation below measures one role on its own cases:

<!-- featured-benchmark:start -->

**Latest frozen confirmation:** `mother-in-law` met **5/5** reviewed interaction-QA targets versus baseline **5/5**, with **0** skill false positives. Across 5 new cases committed before execution, the skill used **93.2%** normalized total tokens and **71.3%** normalized elapsed time. This is one fresh session per arm and task, not a whole-team or repeated-sample claim.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="benchmarks/results/mother-in-law-confirmation-2026-09-12/comparison-dark.svg">
  <img src="benchmarks/results/mother-in-law-confirmation-2026-09-12/comparison-light.svg" alt="5-task frozen mother-in-law confirmation: baseline meets 5 of 5 reviewed targets and skill meets 5 of 5; normalized tokens 100 and 93.2 percent; normalized elapsed time 100 and 71.3 percent." width="100%">
</picture>

[Inspect the frozen cases, raw values, method, and limitations](benchmarks/results/mother-in-law-confirmation-2026-09-12/README.md).

<!-- featured-benchmark:end -->

[Historical integration06](benchmarks/ALL-EIGHT-CURRENT-06-REVIEW.md) and
[earlier team comparisons, adverse outcomes and per-tool experiments](docs/ONBOARDING-HISTORY-2026-09-28.md)
remain available. Local tests, hosted checks and model measurements establish
different things; a favorable case does not prove whole-team savings.

<a id="the-test-passed-the-record-disappeared"></a>

## One example

In a Con Artist audit, a test that checked only `save(...)["ok"]` still passed after
the actual write was removed in a disposable copy. Checking the stored record
caught the defect. Production code stayed intact; the no-skill baseline also found
it. [Compare the original runs and try the helper](examples/con-artist.md).

<a id="why-astra"></a>
<a id="were-unfortunately-hiring"></a>

## Contribute

A hire needs a distinct job, a realistic example and a case where it should leave
things alone. [Contribution guide](CONTRIBUTING.md) · [Security reporting](SECURITY.md) ·
[Design rationale](docs/ASTRA.md) · [Release readiness](docs/RELEASE-READINESS.md) ·
[Roadmap](docs/ROADMAP.md) · [Changelog](CHANGELOG.md) · [MIT license](LICENSE).

<a id="inspiration"></a>

Inspired by [Ponytail](https://github.com/DietrichGebert/ponytail): memorable characters
carrying concrete engineering habits. Our team, instructions and fixtures are original.
