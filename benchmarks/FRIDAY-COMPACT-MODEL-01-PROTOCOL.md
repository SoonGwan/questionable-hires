# Friday compact entry: direct old/new development comparison

Freeze original `b2816cd` versus candidate `e063131`. Resource inventories differ
only at friday/SKILL.md; scripts, references and metadata are byte-identical.
This isolates the changed input, not a causal effect from one model run.

Three existing exposed authored tasks, unchanged:

- rolling-schema from bundle-contract-v2-cases.json, SHA-256
  `1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65`.
- quota-overlap-gap and quota-overlap-control from friday-writer-cases.json,
  SHA-256 `7f61ee6e426636279085446bf5dc1f1c9c09b8b68f48f532d82eda6c80412341`.

The writer cases use actual Python application functions over SQLite; they are
not another database engine, multiconnection transaction or production test.
No new fixture or criterion is introduced. Release contracts remain visible in
the supplied projects. Review actual writer/reader binding and acknowledged
updates/inserts, not merely helper execution or a SELECT success flag.

Before launch, native fixture test confirms the gap's stale/null values and
lost new update after down, while the synchronization control preserves all
values. The existing matrix's 33 tests pass. Three new orchestration tests pass:
frozen resources/cases, six-session settings, terminal failure retention and
account-limit/missing-manifest stopping. Prior full local suite: 458 passes,
70.722s. These are local checks, not hosted CI or model evidence.

Six serial fresh explicit-Friday Astra medium sessions, n=1 per task/version,
240 seconds/cell, jobs=1, seed20260911. Order is original/candidate for schema,
candidate/original for writer gap, original/candidate for writer control. No
no-skill arm: this asks whether compression improves the preceding skill, not
whether either version beats a baseline. Orders are not fully counterbalanced.

Preserve all attempts, errors, output gaps, timeout/unknown usage and extra work.
Never subtract reconnect costs or replace original logs with author replay.
No resource/task edits or author tests during timing. No favorable-result retry;
stop new scheduling after account limits or missing runner completion. Poll a
live handle after observation timeouts rather than restarting it.

After all six terminal sessions: inspect conclusions, actual function/query
execution, data surviving rollback, output completeness and original-file scope;
reconcile raw usage and frozen installed resources. Report every pair. Aggregate
only known complete usage, cached input counted once plus output. Exposed n=1
tasks/shared host/cache/unequal extras prohibit a general efficiency claim.
Update dated EN/KO status; leave historical/featured charts unchanged.

```sh
python3 -B benchmarks/run_friday_compact_01.py --output benchmarks/local-runs/friday-compact-model-01
```
