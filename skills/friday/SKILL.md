---
name: friday
description: Review a planned deployment or release diff for rollback feasibility, mixed-version compatibility, migrations, and configuration readiness without deploying it.
---

# Friday

> Can Monday-you undo this?

## Read Monday's incident report early

Identify the release diff, deployment order, runtime versions that may coexist, and the rollback mechanism. Inspect migrations, configuration changes, jobs, and consumers relevant to that release. Don't assume a rolling deployment or zero-downtime requirement if the project uses a different documented strategy.

Walk the documented release one step at a time. At each reachable state, identify active readers/writers and the data/configuration they see; then walk rollback from that state, including data already written by new code. Test incompatible pairs, not an imagined deployment strategy. Include queued work or external effects only when this release changes their contract.

Separate reverting application code from reversing data changes. A down migration can exist while losing data. Backups are not a proven recovery path without relevant restore evidence. Look for an expand/migrate/contract sequence when a destructive schema transition must coexist with older consumers.

Find the earliest incompatible or irreversible step and the last recoverable state. Tie each blocker to that transition and the smallest compatible ordering or prerequisite. A local SQL check proves that SQL behavior, not production readiness. Use designated staging only when authorized; review never authorizes deployment, production migration, or restore drills.

## Deliver and stop

Lead with ready, ready with stated conditions, or blocked by specific evidence. Use unknown where configuration or runtime evidence is missing; don't label an untested release safe. For each consequential finding include the affected step, failure mode, evidence, and actionable mitigation or verification.

Stop after the release's material compatibility and recovery paths are assessed. Don't perform a generic infrastructure audit. If a fix was requested, prepare the scoped correction and verify it without silently releasing it.

## Working agreement

Preserve user changes and explicit requirements. Review is not permission to implement or publish. Separate observed evidence from inference; keep humor optional. Reuse existing artifacts and report decisive evidence without duplicating full logs.
