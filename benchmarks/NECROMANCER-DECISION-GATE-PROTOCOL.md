# Current necessity versus historical explanation

Candidate hypothesis: remove mandatory history collection when an explicitly
removal-only decision is already settled by an observed break in a required
current caller. This is not a claim that reading fewer instructions or running
fewer shell calls reduces total session cost. The entrypoint gains a decision
gate; the collector and its interface are unchanged.

The previous [nearby-history comparison](HISTORY-REGIONS-01.md) remains adverse.
It required historical investigation and does not demonstrate waste that this
gate would have prevented. Do not rerun that task expecting the new gate to
remove requested historical evidence.

## Next behavioral screen

Use two related requests on the same frozen legacy-code fixture, one repeat per
condition, fresh serial Astra medium sessions and a 240-second per-cell limit.
Compare the predecessor entrypoint at `8844685` with this candidate, not merely a
no-skill baseline. Freeze fixture bytes, both resource inventories, user prompts,
criteria and the scheduled order before launching. No retries or exclusions.

- Removal-only request: assess whether a particular fallback can be deleted.
  The supplied current consumer requires it. Accept an actual current-path
  counterexample and a supported retain recommendation without Git attribution;
  historical investigation is allowed, but record whether the gate avoids it.
- Historical request: explain when and why that fallback was introduced and
  whether it is still required. Require relevant before/after historical evidence
  plus the live contract. Skipping history is a regression, even if faster.

Do not expose the intended conclusion or these criteria to the model. Keep the
visible tasks ordinary user requests, and retain originals, tool outputs, final
answers, diffs, usage and resource hashes. Verify that each observed failure is
the actual proposed removal's effect, not setup or import failure. Neither review
request authorizes permanent implementation changes.

Judge scope and evidence before comparing whole-session input-plus-output tokens
and wall time. Inspect adopted workflow, not just final wording. Any missing
required history or current contract rejects the candidate on that task. A
two-request development screen cannot establish broad superiority; even a clean
win needs transfer beyond the shared fixture. No model results exist for this
candidate yet.

## Frozen inputs and order

Generate the two inputs with `python3 -B benchmarks/decision_gate_cases.py
--output <new-file.json>`. The generator reuses `history_region_cases.py`; these
are request-scope variants of exposed development data, not new independent
projects. Freeze both generators at this protocol update's commit before a run.

Export the entire `skills/necromancer` tree from predecessor `8844685` and
candidate `0143ef2`, preserving file modes. Record each exported file's SHA-256
and the generated task JSON digest before execution. Evaluate exported snapshots,
not the mutable worktree, with `run.py --arms skill --jobs 1 --repeats 1
--model gpt-6-astra --effort medium --timeout 240 --seed 20260911` and the
corresponding `--skills-root`, `--cases-file`, `--case` and fresh `--output`.

The fixed serial order is removal/predecessor, removal/candidate,
origin/candidate, origin/predecessor. Each invocation selects exactly one case.
Stop scheduling on an account limit or incomplete orchestration; do not restart
or silently replace a cell. Four model sessions total, no baseline arm.

Author fixture checks execute the actual consumer with original and altered
module bindings. Current code passes all four tests; removing the code fallback
produces one assertion failure and two missing-code errors. The introducing
commit changes direct indexing to the fallback. Original files and Git status
remain unchanged. All three history-transfer fixture tests pass locally. These
checks validate the task mechanism, not the candidate model's behavior.
