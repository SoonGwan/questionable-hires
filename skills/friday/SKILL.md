---
name: friday
description: Review a planned deployment or release diff for rollback feasibility, mixed-version compatibility, migrations, and configuration readiness without deploying it.
---

# Friday

> Can Monday-you undo this?

## Read Monday's incident report early

Start from the supplied release diff and documented deployment/rollback order. Resolve the actual old/new artifacts needed for the reachable states; use Git history when a version, changed contract or migration sequence is unresolved, not to collect commit metadata after those artifacts are already established. Identify relevant configuration and consumers without imposing rolling deployment or zero downtime on a different strategy.

Map reachable rollout and rollback states to the active readers/writers and their data/configuration, including data written by new code. Choose compatibility witnesses from actual branches, representation boundaries and state-changing transitions. A finite input range alone does not require exhaustive enumeration; expand coverage when value-dependent behavior or the requested assurance warrants it. Establish each distinct pairing, then reuse evidence only while code, inputs and relevant runtime state are unchanged. A different phase label alone needs no repeated execution. Changed data, configuration, side effects or ordering can invalidate that evidence: recheck affected pairings, not just the pre-change state. Include queued work or external effects only when this release changes their contract.

Separate reverting application code from reversing data changes. A down migration can exist while losing data. Backups are not a proven recovery path without relevant restore evidence. Look for an expand/migrate/contract sequence when a destructive schema transition must coexist with older consumers.

Locate the first incompatible or irreversible step and last recoverable state. Tie blockers to that transition and the smallest compatible ordering or prerequisite. Local SQL proves SQL behavior, not production readiness; use staging only when authorized.

Choose the execution path from the contract before opening tool references. If the evidence depends on application writer functions, transaction boundaries or multiple connections, exercise those actual functions and runtime facilities; the SQL reader matrix cannot substitute for them. For repeated SQL-only SQLite reader checks across migration states, the optional [in-memory matrix interface](references/sqlite-matrix.md) avoids rewriting the loop. Read it only for that path; source inspection is for trust, adaptation or troubleshooting. Keep simple checks on the existing runner; don't translate another engine's migrations to SQLite.

## Deliver and stop

Lead with ready, ready with conditions, or blocked by evidence. Mark missing runtime/configuration evidence unknown, not safe. Give each consequential finding's step, failure, evidence and mitigation without repeating full logs.

Stop after the scoped compatibility and recovery paths are assessed, not after a generic infrastructure audit. Preserve user changes and requirements. Review authorizes neither implementation nor deployment, production migration, restore drills or publication. If a fix was requested, verify the scoped correction without releasing it.
