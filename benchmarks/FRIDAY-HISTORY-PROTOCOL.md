# Necessary-history release transfer

Two new development cases, not confirmation data. Current project files are
byte-identical; only deployed worker history differs. One old worker cannot read
new payloads; the other can. Queued work survives rollback. This requires actual
historical artifacts, providing a counterweight to the new conditional-history
routing. The author-only fixture test executes both generations from real Git
history and verifies their different conclusions. Do not supply that test or this
assessment to evaluated models; run.py supplies each case's neutral task only.

Use Friday `debf188`, freeze fixtures and source at the protocol commit before
execution. Four fresh Astra medium sessions, one sample per case/arm, serial,
240-second limit, seed 20260911, no retries/exclusions:

1. worker-history-gap: skill
2. worker-history-gap: baseline
3. worker-history-compatible: baseline
4. worker-history-compatible: skill

Generate a fresh ignored cases JSON with friday_history_cases.py. Preserve all
criteria, original logs, file/resource identities, failures and total tokens/time.
Inspect actual producer/worker execution, mixed-version and rollback queue
reasoning, history lookup and unverified operational limits. Do not require a
helper or real queue infrastructure absent from the fixture; no installation,
network, deployment or changed original files. Compatible payload handling does
not establish operational readiness. Retain costs even if extra checks are useful.
One pair per task is not stable or causal performance evidence. Do not rerun the
previous exposed SQL rename case to chase a favorable result.
