# Receipt tree guard adoption 01 — 2026-09-14

Freeze resources `ec0cc28`; unchanged `receipt-src-cases.json`, SHA-256
`2ca86a989d524318d47a96f46053a79aff16f551a439f7d47d898a336ed87d07`.
One exposed explicit-skill Astra medium session, serial n=1, seed20260911,
240-second bound, no retry. No edits or author workloads during timing.
Preflight: eight guard tests (nine native mutation subcases), 47 existing helper
and 12 packaging tests pass; native fixture/tests remain unchanged.

Review actual guard adoption and whether custom inventory code/hash listing is
removed. Neither is itself the task success criterion. Require original native
five-method before/after suite, two defect-specific failures and three controls
before, five passes after, copied imports, fixed current tests/samples, identified
HEAD/working content, unchanged originals and cleanup with no extra harness or
report. Preserve any extra work, capture gaps, missing evidence or rejected input.

After timing reconcile raw events/usage, frozen resources and fixture content.
Replay the literal recipe/program separately; inspect any inventory digest change
against actual filesystem differences instead of normalizing it away. Collector
postprocessing can modify Git index after model execution; distinguish those
changes from original observations. Do not fill original gaps with author replay.

Report absolute cost and descriptive comparison with output-choice 01. Exposed
task, n=1, shared cache and unequal work prevent causal/general efficiency claims;
no contemporary baseline. Historical/featured graphs stay unchanged. Record both
languages in current status, not another long landing-page experiment paragraph.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/receipt-src-cases.json --output benchmarks/local-runs/receipt-tree-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
