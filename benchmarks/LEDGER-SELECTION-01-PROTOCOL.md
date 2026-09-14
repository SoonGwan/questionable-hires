# Ledger test-selection screen 01 — frozen before model execution

Candidate resources `f9844ad`; one new authored SQLite transaction-audit task,
not a real-repository holdout. Baseline and skill, one repeat each, Astra medium,
serial, seed 20260915, 240 seconds/cell. Both explicitly persist session records
for matching tool-response extraction. Preserve all scheduled outcomes, no retry.

The task requires the same six native test processes in both arms: one correct
and one faulty execution for each of three methods, no extra grouped suite or
stronger probe. The fault changes only error-path rollback into commit. The
model-visible request explicitly specifies process exits, real implementation,
original preservation, project-local scratch and final removal. The helper is
optional; no prompt names batching or supplies its recipe. Existing small-audit
native-tool routing stays in force. This task intentionally exercises the newly
supported selection boundary; it is not independent proof of broad usefulness.

[Native preflight](ledger-selection-01-preflight.json) runs exactly the six
checks through unchanged unittest. Correct code: all three pass. Faulty code:
exception-only and success-path checks pass; persisted-balances assertion fails
with actual source balance 90 versus expected 100. No setup error supplies that
failure. All test-created temporary directories are inside their disposable
projects and removed. Generator and frozen input are retained.

Review criteria:

1. Inspect actual commands, tool responses and assertion paths, not just model
   conclusions. Report per-method normal/faulty exits and the persisted debit.
2. Verify copied/imported implementation provenance, unchanged original bytes,
   scoped fault, six executions and scratch cleanup. Do not assume helper use.
3. Reconcile CLI usage and complete tool records from each exact new stored
   session. Keep full rollout context local; export reviewed tool excerpts only.
4. Token metric is input (cache included once) + output; elapsed is full CLI wall
   time. A cost reduction with missing evidence, unequal work or invalid checks
   is not an accepted efficiency win. n=1 and shared host/cache prohibit broad
   causal claims even for a clean favorable pair.

Do not rewrite prior screens, criteria, featured graphs or README numbers.

Launch:
`python3 -B benchmarks/run.py --cases-file benchmarks/ledger-selection-01-cases.json --arms baseline skill --repeats 1 --jobs 1 --seed 20260915 --timeout 240 --model gpt-6-astra --effort medium --persist-session --output benchmarks/local-runs/ledger-selection-01`
