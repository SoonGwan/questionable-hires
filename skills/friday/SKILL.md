---
name: friday
description: Review a planned deployment or release diff for rollback feasibility, mixed-version compatibility, migrations, and configuration readiness without deploying it.
---

# Friday

> Can Monday-you undo this?

## Read Monday's incident report early

Read the release diff, deployment/rollback order and known old/new artifacts together. Discover missing consumers/configuration; use history only for unresolved versions, contracts or migration order. Don't impose rolling deployment or zero downtime on another strategy.

Exercise reachable reader/writer and schema/configuration pairings, including new-version writes before rollback. Choose witnesses from actual branches, representation boundaries and transitions; enumerate further when value-dependent behavior or requested assurance warrants it. Reuse results only while code, inputs and relevant state remain unchanged: a new phase label alone needs no rerun, but changed data, configuration, effects or order may. Include queued/external work when its contract changes.

Reverting code is not restoring data. Inspect what survives down, including current new-version writes; a backup needs restore evidence. Consider expand/migrate/contract when destructive schema changes must coexist with older consumers.

Choose the runner before reading tool references. Actual application writers, transactions and multiple connections need their real runtime. For repeated SQL-only SQLite reader checks, use the optional [matrix interface](references/sqlite-matrix.md) when no adequate runner exists. Simple checks stay on the existing runner; never translate another engine's migrations to SQLite. Inspect helper source for trust, adaptation or troubleshooting, not routine invocation.

## Deliver and stop

Lead with readiness, the first incompatible/irreversible step and last recoverable state. Tie each blocker to evidence and a compatible ordering or prerequisite. Missing runtime/configuration evidence is unknown; local SQL is not production readiness. Don't repeat full logs.

Stop after scoped compatibility and recovery checks. Preserve user changes and requirements. Review does not authorize edits, deployment, migration, restore drills or publication; staging needs authorization. A requested fix includes verification, not release.
