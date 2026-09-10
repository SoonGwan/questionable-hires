# Performance reviews

Metadata validation is not behavioral validation. Installer tests are not model benchmarks. This document defines the cases needed to evaluate each hire; results must be recorded separately after execution.

## Case matrix

| Hire | Positive case | Clean or limiting case | Evidence required |
| --- | --- | --- | --- |
| Necromancer | A delayed navigation hides an unfinished save; history identifies the original race | The caller now awaits persistence; a second fixture has no history | Current call path, historical facts separated from inference, keep/replace/remove recommendation |
| Receipt | An off-by-one limit rejects the first valid value | Fix exists but the old revision cannot run | Same input and meaningful assertion before/after; unavailable before evidence stays unavailable |
| Landlord | A single fixed formatter has an unused provider registry | A single-consumer adapter protects a volatile external contract | Actual consumers and justified costs; no automatic rejection of a legitimate boundary |
| Mother-in-law | Two overlapping searches show an older response last | Requests already use generation checks | Controlled response order, user-visible state assertion, no hypothetical defect reported as observed |
| Exorcist | A stale result resembles a cache problem but correlates with response order | Runtime access is missing | Experiment distinguishing cache reuse from ordering; honest uncertainty if it cannot run |
| Hostage Negotiator | A label change comes with an optional state-management rewrite | A requested new state really requires changing state handling | Requested behavior delivered; necessary prerequisite retained; unrelated refactor excluded |
| Con Artist | A mocked service test never checks persistence | A fault is equivalent on the test's intended domain | Baseline pass, meaningful isolated fault, survivor or kill, restored production behavior |
| Friday | A schema rename breaks the old binary during rolling rollout | An additive nullable field preserves both readers | Compatibility evidence, specific risky rollout step, rollback limits; no deployment performed |

For Necromancer also include a compatibility branch with an active supported consumer. A comment saying “legacy” is not permission to remove it.

## Run record

Record: date, skill revision, fixture revision, model and reasoning setting, host version, loaded instructions, exact user request, allowed actions, commands, exit statuses, output artifact paths, and reviewer findings. Note unavailable token or time metrics explicitly.

Score correctness and scope separately. A correct diagnosis accompanied by unauthorized modifications is not a successful run. A clean review with evidence is a success; manufacturing a defect is a failure.

## Current evidence

The automated suite checks installation, bundle construction, catalog structure, and fixture behavior. Actual independent Astra sessions have also been run: 24 three-arm comparisons, eight additional skill-only cases, and a separate three-run pilot. See the [report and execution evidence](../benchmarks/REPORT.md). These are small synthetic smoke tests, not a demonstration of broad superiority. Repeated trials and larger real-project tasks remain necessary before making performance claims.

A separately preregistered 72-session, three-repeat comparison completed on September 11. See the [new report](../benchmarks/REPORT-2026-09-11.md), including strict criterion/scope failures, unknowns, resource increases and independent checks. Earlier smoke runs are excluded. Real-repository effectiveness remains unmeasured.
