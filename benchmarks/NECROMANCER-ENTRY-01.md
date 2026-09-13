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

## Result — 2026-09-14

Candidate/launch `d5c7150`. Entrypoint bytes decreased 3,490 → 2,310 (33.81%);
conditional guidance remains in the existing reference. Skill metadata validation,
23 actual history-helper tests (5.215s), and two fixture tests including native
preflights (0.222s) passed before launch. These do not prove agent behavior.

Both scheduled attempts are retained. Skill timed out at **240.025s**, exit −15,
with only thread.started and turn.started events: no captured skill read, tool
execution, answer, or terminal usage. Usage is **unknown, not zero**. The evidence
does not identify whether the wait was service, transport, runtime or model-side;
it does not establish an instruction-caused regression or successful adoption.
No retry was scheduled.

Baseline completed in **31.418s / 63,924 tokens**, three shell calls. It reads
actual source/history, cites the introducing compatibility commit, verifies the
current consumer returns Ada and demonstrates missing-display alternatives, and
correctly recommends retaining the fallback. Its consumer link points at the
nearby support comment rather than the call itself. Native output is captured.

Original/redacted event streams reconcile and installed before/after manifests
are unchanged. No useful token ratio or equal-quality efficiency claim can be
computed. A timeout-to-completed wall-time ratio is not a task-speed comparison.
The candidate remains behaviorally unverified; gate 05 remains the latest complete
bundle evidence. [Every attempted cell](results/necromancer-entry-01/README.md)
is preserved, including the timeout and null usage.
