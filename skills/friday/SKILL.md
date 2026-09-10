---
name: friday
description: Review a planned deployment or release diff for rollback feasibility, mixed-version compatibility, migrations, and configuration readiness without deploying it.
---

# Friday

> Can Monday-you undo this?

## Read Monday's incident report early

Identify the release diff, deployment order, runtime versions that may coexist, and the rollback mechanism. Inspect migrations, configuration changes, jobs, and consumers relevant to that release. Don't assume a rolling deployment or zero-downtime requirement if the project uses a different documented strategy.

Follow compatibility in both directions: can old code read data written by new code, and can new code tolerate old data and missing new configuration during rollout? Examine renames, drops, backfills, queue payloads, and irreversible external effects when present.

Separate reverting application code from reversing data changes. A down migration can exist while losing data. Backups are not a proven recovery path without relevant restore evidence. Look for an expand/migrate/contract sequence when a destructive schema transition must coexist with older consumers.

Check observable readiness and a concrete rollback trigger against the documented operating context. Use local or designated staging checks when authorized. Reviewing a release does not authorize deployment, production migration, or a restore drill.

## Deliver and stop

Lead with ready, ready with stated conditions, or blocked by specific evidence. Use unknown where configuration or runtime evidence is missing; don't label an untested release safe. For each consequential finding include the affected step, failure mode, evidence, and actionable mitigation or verification.

Stop after the release's material compatibility and recovery paths are assessed. Don't perform a generic infrastructure audit. If a fix was requested, prepare the scoped correction and verify it without silently releasing it.

## Working agreement

Follow the user's requested outcome and repository conventions. User instructions take precedence over this skill's preferences. Resolve routine choices from available context and keep working within authorized scope. Investigation is not permission to implement or publish. Preserve existing user changes.

Use the user's language. Keep the character to an optional short line; never insult people or substitute a joke for evidence. Report observed facts separately from inferences and unavailable checks. If a skill instruction actually prevents progress, cite that instruction and explain the concrete conflict.

