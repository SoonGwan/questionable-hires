# JavaScript lifecycle wrapper development screen

Frozen candidate: `22bd929`. Unchanged task source:
`hostage-javascript-panel-cases.json`, SHA-256
`20545c1e08faf86c67f228c935dce74e947fb1faf983dcce0becbe99290c199c`.
This is an exposed development task, not an independent holdout.

Motivation and native contract: [lifecycle candidate](HOSTAGE-JAVASCRIPT-SCOPE-01.md).
No task/criteria changes relative to the previous panel screen. All transitions,
original-test preservation, bounded cleanup, real abort rejection, project scope
and original native result evidence remain required. The helper is not injected
into the baseline. No reference solution or author controls enter either project.

Preflight at candidate: 470 local tests passed in 68.700s, no failures/skips,
including 17 native helper tests and existing author panel positive/negative
controls. Skill/repository/featured-language validators and diff checks passed.

Run two fresh serial Astra medium sessions, baseline and explicit skill, n=1 per
arm, seed 20260911, jobs 1, 240 seconds per cell. Preserve all scheduled attempts,
timeouts, usage unknowns, scope exceptions and original capture limitations. No
favorable retry. No resource/task edits or author test workloads during timing.

Review actual retained native assertions and implementation, not just completion.
Inspect whether the wrapper is adopted and actually replaces scenario boilerplate,
whether native verification exits/counts are captured, and whether all obligations
remain exercised. Report command count and added support alongside raw token/time
cost. A shorter test file or successful import alone is not a performance gain.
Reconcile original events/resources and exact reviewed inventories after timing;
replay untouched retained tests on final/original/missing guard/missing cleanup/
wrong signal copies with process deadlines. Replay does not repair original output.

Primary comparison is within this fresh pair. Earlier one-pair results are
historical context, not a controlled estimate of wrapper improvement. Shared
host/cache, authored/exposed task, n=1 and differing extra work limit inference.
Do not update featured charts or assert general savings from this development run.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-javascript-panel-cases.json --output benchmarks/local-runs/hostage-javascript-scope-model-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
