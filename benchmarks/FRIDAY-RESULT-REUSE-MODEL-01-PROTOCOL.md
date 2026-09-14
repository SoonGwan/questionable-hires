# Friday result reuse model screen 01

Instruction candidate `e0956d5`; runtime `e3bc342`. This protocol's commit is
launch. Previous turn made progress: core CLI/API routing and a native single-
connection example test were implemented, validated and pushed. No model savings
were claimed. This screen tests whether that route is actually selected.

Use the unchanged author-exposed `binary-rollback` task in
`friday-binary-rollback-cases.json`, SHA-256
`e81ecad7fd169c0c34d00d25be3fcb13bcd76eaa990857d77b36ecfc78b9371f`.
The existing native correct/incorrect rollback controls and explicit task
contracts remain unchanged. Two fresh serial sessions: baseline/skill, n=1,
Astra medium, seed 20260914, 240 seconds each. Preserve every attempt, incomplete
usage, capture/connection errors and adverse outcome. No favorable-result retries.
Stop new scheduling on account limits. No skill/task edits or author tests during
timing; poll confirmed live handles rather than restarting on observation gaps.

Review actual supplied readers, four migrations/stages, storage/value types,
current expected versus down bytes for updated/untouched/inserted/empty rows,
and the stopped-consumer maintenance strategy. No inferred irreversible loss,
application-writer or staging claims. Preserve originals and project scope.
Record core/detail loading, CLI/API/custom-loop choices, repeated execution,
assertions and any unequal work. Helper adoption and avoiding a repeat are not
scored obligations; missing necessary verification is not a cost saving.

Reconcile raw usage/events/resources/snapshots only after timing; export every
cell and review native output against claims. Keep author replay separate.
One exposed task, n=1 and shared host/cache do not establish causal old/new or
all-eight gains. Preserve past results and featured charts. Update EN/KO status
and capability limitations after review, even for adverse results.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/friday-binary-rollback-cases.json --output benchmarks/local-runs/friday-result-reuse-model-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260914 --timeout 240 --model gpt-6-astra --effort medium
```
