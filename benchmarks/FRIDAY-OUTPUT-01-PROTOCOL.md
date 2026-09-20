# Friday output pilot 01 — frozen before model execution

2026-09-21. Two related authored tasks × baseline/original/candidate × one fresh
session, GPT-6 Astra medium, 360 seconds per cell, serial. Original resources
`75f6b4f`; candidate applies only `friday_output_candidate.revise` from `eaac566`
to `skills/friday/references/sqlite-matrix.md`. The main skill and every other
resource remain byte-identical. Neither candidate nor results are release approval.

## Inputs and schedule

Use `friday-output-cases-01.json`, not live regeneration. Fixed order: contracts
baseline → contracts original → contracts candidate → observations candidate →
observations original → observations baseline. Invoke `run.py` with one `--case`,
`--arms baseline` or `--arms skill`, `--repeats 1 --jobs 1 --seed 0 --timeout 360
--model gpt-6-astra --effort medium --persist-session`, separate fresh output and
workspace per cell. Verify resource identities before execution and preserve all
scheduled cells, including unattempted ones on account limits. No retries, fixture
changes, replaced attempts or outcome exclusions after launch.

Both tasks use the same small SQL project but differ in requested output. This
paired construction tests output-mode adaptation, not independent generalization.
OLD requires total stock; NEW requires available stock. The proposal accidentally
changes OLD to available stock while preserving column names. It first conflicts
with the representative data after reserved stock is written at step 3, not on the
schema change at step 2. A no-SQL OLD restart does not fix it. Down restores OLD
and keeps all stored quantities/reservations. An inactive NEW failure at step 1
is not a release blocker. Both consumers are explicitly requested at all five
phases, even when inactive; coverage cannot be removed for cost reduction.

The contracts mode asks for concise evidence-backed findings, not full raw JSON.
The observations mode additionally requires a complete machine-readable record of
all observations/errors/completion/truncation and reader file/constant/line/hash/SQL
provenance. Both require actual execution, full ordered row/column comparisons,
rollback data preservation, supported mitigation, unchanged files/Git state and no
leftover scratch. All scored duties are model-visible, not surprise author demands.

## Author controls and evidence

`friday_output_cases.py` produces the inputs and preflight. The frozen
`friday-output-preflight-01.json` retains three separate native SQLite matrices:
the actual proposal, stored-data survival inspection, and an author-only compatible
proposal using the original total-quantity view. Ten actual reader observations
include seven contract passes, two expected OLD row assertion failures, and one
inactive NEW error. Failures retain phase/check and expected/observed values.
The compatible proposal passes OLD at all five phases. Source bytes are preserved;
temporary directories are project-local and cleaned up. No author-only correction,
oracle or preflight record is installed into a model project.

Four local tests cover candidate isolation, native assertion controls, case-mode
differences, exact frozen-input/preflight equality and provenance. They do not
prove model behavior. These cases are authored synthetic tasks, not real issues or
blind holdouts. The exposed screen03 view-contract task must not be rerun for selection.

## Review and adoption gate

Review all five criteria in each original session's commands/results/artifacts.
Do not infer coverage from helper completion or a final PASS label. Check executed
queries/SQL, complete rows and zero values, actual rollback storage, inactive versus
active failures, correct transition ordering and source provenance. Review scope,
HEAD/index/resources and scratch inventory. Original assertion failures and setup
errors are different; author replay is separate from original model evidence.

Reconcile input+output tokens (cache counted once), wall time, recorded responses,
success/scope and required-output completeness. Inspect exact initial skill exposure
privately; never export private initial messages. Preserve every cell, including
adverse results. Less output with missing raw observations/provenance is a failure,
not efficiency. Optional helper adoption is not a pass criterion.

Compare candidate with contemporary original and no-skill baseline in each output
mode. Report unequal work and any later rereads. No n=1 favorable pair establishes
a broad gain; retain production resources unless reviewed evidence supports adoption.
No frozen graphs, historical measurements or featured pointer change from this pilot.

한국어: 같은 SQL 프로젝트에 계약 검토와 원본 관측 출력이라는 서로 다른 요청을
주고 무스킬·기존·후보를 총 6회 비교한다. 출력량이 줄어도 행·열·롤백 데이터나
요청한 원본·출처가 빠지면 개선으로 보지 않는다. 요구사항과 실제 정상·결함 대조를
먼저 고정했으며, 모델 결과가 나오기 전에는 채택하거나 성능 수치를 주장하지 않는다.
