# Necromancer entrypoint candidate 01

Gate 05 history review used 34.51% more tokens and 22.44% more time with the skill.
It repeated known-file discovery and keyword matching despite focused attribution.
The new candidate consolidates entry instructions around current necessity versus
historical origin, explicitly batches known implementation/consumer reads, and
moves conditional pickaxe/rename/bulk-patch guidance into the existing reference.
The collector and its safeguards are unchanged. This follows skill-creator's
progressive-disclosure guidance; reduced instruction bytes are not measured
model-token savings, and more terse instructions need behavioral verification.

Prospective check: unchanged `history-active` from bundle-contract-v2-cases.json,
SHA-256 `1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65`.
One baseline and one explicit skill session, fresh serial Astra medium, seed
20260913, 240-second limits. No retries/exclusions or task/resource edits during
timing; no concurrent author test workloads. Preserve account/capture/scope issues.

Review the actual current caller, relevant historical commit, origin/necessity
distinction and preservation of project files. Retain extra work and missing
evidence; do not claim efficiency from omitted required verification. Sum input
plus output with cached input once and report wall time. This exposed n=1 task
is not causal confirmation, independent transfer, or the all-eight objective.
Keep gate 05 and featured/localized charts tied to their measured resources.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/bundle-contract-v2-cases.json \
  --case history-active --arms baseline skill --repeats 1 --jobs 1 \
  --seed 20260913 --timeout 240 --model gpt-6-astra --effort medium \
  --output benchmarks/local-runs/necromancer-entry-01
```
