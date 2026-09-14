# Receipt native invocation adoption 01 — 2026-09-14

Freeze resources `bc3b225`; unchanged ledger cases SHA-256
`5aeac6200940dc4d29898920429aae684712afea753df12e7985862f5016b742`.
Two explicit-skill sessions, Astra medium, serial n=1, seed20260911, 240 seconds
each, no retries. No resource edits or author workloads during model timing.
Preflight: 82 related tests pass, including literal native-module execution of
both frozen SQLite variants, same-process imports, failure/cleanup controls.

Require the unchanged five current native tests/schema in both committed revisions,
copy-local imports, identified revisions and actual outcomes. Both before variants
have two retry failures/three controls; complete after passes five, partial after
still has two balance failures. Preserve originals, ignored cache and notes;
remove owned copies/databases without retaining a harness/report. Record actual
invocation adoption and any internal adapter separately from correctness.

After timing reconcile raw/events/usage, frozen resources, project files and
pre-collector index. Replay the actual literal program/recipe separately in
disposable copies, retaining any index changes, diagnostic/output mismatch and
original capture gaps. Never fill missing original evidence using author replay.

Compare descriptively with both prior skill sessions and prior baselines from
ledger-01; no contemporary baseline, exposed correlated tasks, shared cache and
unequal work prevent causal/general efficiency claims. Preserve adverse results
and all scheduled cells. Do not change historical/featured charts. Update dated
review and EN/KO current status, not lengthy landing-page experiment paragraphs.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/receipt-ledger-cases.json --output benchmarks/local-runs/receipt-native-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
