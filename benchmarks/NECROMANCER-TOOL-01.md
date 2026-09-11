# Necromancer collector: candidate, not an efficiency win

One `history-active` skill sample at `fa3fab7`, under ignored
`local-runs/necromancer-tool-01`, completed in 29.096 seconds using 75,740
total tokens (75,154 input including cache, 586 output). The earlier
`fast-regression-02` sample used 67,441 tokens and 28.163 seconds.
These temporally separated single samples show no efficiency improvement.

The answer correctly preserves the fallback based on the live partner caller
and cites the introducing commit. The recorded diff is empty. However, both
original and processed event logs contain an empty aggregated output for the
collector invocation despite exit code zero. Do not credit those logs as a
captured historical-evidence chain. An independent local replay against the
retained project emitted valid JSON with the cited introducing commit and
patch; this confirms the facts, not what output the model saw originally.

Observed avoidable work: the agent loaded the entire helper source and selected
both the declaration and changed behavior, collecting an unrelated initial
commit. The follow-up instruction routes normal use through the interface,
reserves implementation inspection for diagnosis/adaptation, selects only
behavior-changing lines, and favors native Git for one missing fact. This
instruction change is not yet behaviorally measured. A CLI regression checks
nonempty parseable output and attribution limited to the selected behavior.

The collector remains optional. Existing dirty-line, rename, shallow-history,
untracked/non-Git, omitted-commit and read-only checks cover mechanics, not
all-skill performance. No new superiority chart is justified.
