# Mother-in-law contract-expectation checkpoint

Candidate `a2fc7d3`, including the Mother-in-law instruction correction at
`a6574e9`. Run only unchanged `search-order` from bundle-contract-cases.json
(whole-file SHA-256 `3ed27c165bbf688aafdb2bd9c4b1fd68b6b2fe8861bef27551127a7f655ebdea`).
One fresh baseline and one fresh skill session, Astra medium, serial, seed
20260913, 240-second caps. No retries, exclusion, skill/input edits or author
test workloads during timing. Keep account-limit/capture failures as evidence;
do not restart a live process after observation loss.

This targeted follow-up is justified by a changed instruction and the confirmed
correction-incompatible tests in checkpoint 04. It is not another all-eight
checkpoint or an unchanged-candidate rerun for a favorable percentage. The task
is exposed authored development input, not an independent holdout or real-world
confirmation. The broader eight-skill objective remains open.

Before scheduling, rerun the seven fixture behavioral preflights and single
generator-integrity test. The former exercise controlled real Search sequences,
normal/protected controls, intended stale-value assertions and bounded cleanup.
No model-visible inputs or original criteria change. The new diagnostic below
does not retroactively alter prior scores.

Review captured native assertions for normal and reversed overlapping requests,
real Search binding, bounded waits/owned-task cleanup, scope and unchanged
production. Preserve all final deliverables and output gaps. After all timing,
replay each retained test unchanged in separate copies against original Search
and an author-only generation guard. The guard retains existing display until
the latest operation completes and ignores older completions; no production fix
is supplied to the models. Record whether retained tests reject this valid path
through an unspecified intermediate-state expectation. Do not repair their tests
to count a pass. Author replay is not original model execution evidence.

Report both full costs (input plus output, cached input once; cell wall time),
including unsuccessful cells and unequal extra work. A favorable pair alone
does not establish causal savings, generalization or all-eight acceptance.
Keep featured charts tied to their existing data; this is diagnostic evidence.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/bundle-contract-cases.json \
  --case search-order --arms baseline skill --repeats 1 --jobs 1 \
  --seed 20260913 --timeout 240 --model gpt-6-astra --effort medium \
  --output benchmarks/local-runs/mother-contract-01
```
