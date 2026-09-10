---
name: friday
description: Review a planned deployment or release diff for rollback feasibility, mixed-version compatibility, migrations, and configuration readiness without deploying it.
---

# Friday

> Can Monday-you undo this?

## Read Monday's incident report early

Read the release diff and documented deployment/rollback order. Identify the relevant migrations, configuration, consumers and coexisting versions; don't impose rolling deployment or zero downtime on a different strategy.

At each reachable rollout state, identify active readers/writers and their data/configuration; walk rollback from that state, including data written by new code. Test incompatible pairs. Include queued work or external effects only when this release changes their contract.

Separate reverting application code from reversing data changes. A down migration can exist while losing data. Backups are not a proven recovery path without relevant restore evidence. Look for an expand/migrate/contract sequence when a destructive schema transition must coexist with older consumers.

Locate the first incompatible or irreversible step and last recoverable state. Tie blockers to that transition and the smallest compatible ordering or prerequisite. Local SQL proves SQL behavior, not production readiness; use staging only when authorized.

## Deliver and stop

Lead with ready, ready with conditions, or blocked by evidence. Mark missing runtime/configuration evidence unknown, not safe. Give each consequential finding's step, failure, evidence and mitigation without repeating full logs.

Stop after the scoped compatibility and recovery paths are assessed, not after a generic infrastructure audit. Preserve user changes and requirements. Review authorizes neither implementation nor deployment, production migration, restore drills or publication. If a fix was requested, verify the scoped correction without releasing it.
