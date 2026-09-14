# JavaScript usage-first development screen

Frozen resource `f0b29dd`. Unchanged exposed task:
`hostage-javascript-panel-cases.json`, SHA-256
`20545c1e08faf86c67f228c935dce74e947fb1faf983dcce0becbe99290c199c`.
This tests [usage-first routing](HOSTAGE-JAVASCRIPT-USAGE-FIRST-01.md), not a new
runtime implementation. All original task requirements/criteria remain in force.

Schedule two fresh serial Astra medium sessions, baseline and explicit skill,
n=1 each, seed 20260911, jobs 1, timeout 240 seconds per cell. No helper/reference
answer in baseline; no author controls in either project. No favorable retry,
omitted attempt or resource/task edit during timing. No concurrent author tests.
Preserve timeouts, unknown usage, scope exceptions and original output gaps.

Native preflight: existing seven callback and ten lifecycle tests plus standalone
copy integration pass; executable module source remains byte-identical to
`22bd929`. Previous full suite at that executable resource: 470 tests, no skips
or failures. Current repository/skill/featured-language validators passed.

Post-timing review must inspect actual reads (usage comment versus full module),
copy identity, implementation and retained native assertions for every requested
transition, original tests unchanged, owned cleanup, original test exits/counts,
scope, shell calls and token/time costs. Completion or shorter input alone is
not success. Reconcile raw usage/resources and exact reviewed inventories, then
replay untouched retained tests on final/original/missing guard/missing cleanup/
wrong signal copies with 15-second outer process deadlines. Keep replay separate.

Primary arithmetic is within the new pair. Previous exposed screens are not a
controlled before/after estimate. Report unequal extra work, copied code, shared
host/cache and n=1; no general speedup or featured-chart promotion.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-javascript-panel-cases.json --output benchmarks/local-runs/hostage-javascript-usage-model-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
