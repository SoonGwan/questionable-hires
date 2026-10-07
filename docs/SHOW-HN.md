# Show HN introduction

Prepared for the [official Show HN guidelines](https://news.ycombinator.com/showhn.html).
The repository uses English as its primary language and includes an executable sample.
Korean documentation and the localized website remain available.

Title: **Show HN: Questionable Hires – Eight engineering skills for AI coding agents**

URL: https://github.com/SoonGwan/questionable-hires

## Submission text

I made eight fictional coworkers for AI coding agents. Each character carries a specific engineering habit: Receipt asks for a failing-before/passing-after reproduction; Con Artist checks whether tests still pass when behavior is broken; Exorcist designs experiments to distinguish debugging hypotheses; Friday reviews rollout compatibility and rollback.

They are portable skill files with explicit triggers, boundaries, and stopping conditions, plus optional helpers and real examples. Install one or the team with `npx skills add SoonGwan/questionable-hires`. Installing all eight does not run all eight on every task. There are no background services, telemetry, or model-setting changes.

For a runnable example without a model account, the README includes the Con Artist helper. It runs trusted sample code in disposable copies: removing a write or duplicating it still passes the original acknowledgment-only test, while a stronger stored-record assertion catches both faults. The source remains intact. This is a helper demonstration, not a new model performance result.

The repo is MIT-licensed and a development preview. Whole-team quality and cost improvement remain unproven; unfavorable measurements and limitations are included. English is the primary documentation language, with Korean available.

I would like feedback on whether the roles have useful, distinct triggers, and on situations where a skill should stop or stay out of the way. Examples and evidence are linked from the README.

## Publication status — 2026-10-08

Not published. An authorized submission of the owner's other project from the
same signed-in account returned Hacker News's “Update re Show HNs” page,
announcing temporary restrictions due to a large influx. This project is retained
as a draft while that account is restricted. No alternate title, account or route
was used to bypass the restriction. No reopening date was provided.
