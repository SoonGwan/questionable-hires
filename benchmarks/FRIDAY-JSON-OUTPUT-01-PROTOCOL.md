# Friday JSON output01 — prospective interface comparison, 2026-09-28

Parent `968cf250`. Previous Friday resource `371b4b1e` versus fixed `c9b30fc6`.
Only the helper and its two references differ within Friday; the skill entry is
unchanged. The already-adopted [JSON fix](FRIDAY-JSON-NUMBERS-01.md) preserves
SQLite infinities as explicit JSON tags. Previous CLI0 output is rejected by
JavaScript JSON.parse. This study tests whether that concrete handoff repair
changes model cost; correctness was already measured separately.

## Frozen tasks and permitted work

Two authored [cases](friday_json_model_cases.py): actual SQLite positive/negative
infinity, and an otherwise identical finite-number control. Both also include
finite1.25, BLOB00ff, literal text Infinity, null, duplicate column labels and an
expected missing-table reader. One observed phase, no migration or deployment.
These deliberately exercise the repaired interface; they are not a holdout,
natural helper adoption, a no-skill comparison or representative all-eight work.

Both tasks require exactly one unchanged installed CLI invocation and its original
stdout retained as native.json. Produce report.json preserving every result field
and observation. Only non-finite numeric values may be transformed to the explicit
float_special tags; text, signs, finite values, BLOBs, errors and other evidence
must be preserved. The supplied unmodified Node consumer must execute against
report.json. Both arms may use a local adapter of the original saved observation;
neither may rerun SQL, fabricate a report from expected data or alter the helper.
Only native.json, report.json and optional adapter.py may remain as new artifacts.
Preserve original files, resource bytes/modes and Git state; no external services,
configuration changes, installs, other skills or delegation. Report observed exits,
any serialization repair and the failed reader; complete does not mean safe release.

Native preflight imports the actual public helper in a fresh Python process,
executes each case, passes the actual JS consumer and deliberately corrupts one
numeric value. Negative controls must exit1 with assertion diagnostics containing
the bad actual value, not a support-code exception. Cases, criteria, runner,
protocol, native Node binary hash and both resource snapshots freeze before models.
Scheduler tests use synthetic resources and must pass without Git history.

Four fresh serial gpt-6-astra/medium sessions,360s each,n=1 per cell: special
previous→candidate, finite candidate→previous. Reuse the guarded serial scheduler
and retain execpolicy rules. Same tools/profile; no guest MCP, approval changes,
model switching, retries, replacements or favorable-cell selection. Stop on limit
or incomplete CLI. No author tests or edits during timing. Preserve all attempts.

## Review and decision

Review actual commands, original native output, report transformation, consumer
exit, final answer and preserved inputs/resources. Consumer pass alone cannot
prove all-field preservation. Author parsing of saved artifacts is separate from
original model execution; no replay fills missing model evidence. Count model
responses and reconcile terminal input+output usage, including cached input once.
Report per-task and summed tokens/time, extra reads/executions and unequal work.

Accept only a narrow joint-cost observation if both pairs reduce tokens and elapsed
with correct scoped outcomes and no violations. Otherwise retain the native fix
without claiming model savings. Even passing this gate cannot prove causality,
general savings or all-eight superiority: authored n=1 cases, shared host/cache
and differing instruction exposure remain limitations. No unchanged retry, featured
promotion, frozen-chart rewrite or general landing metric update follows this run.

한국어: 실제 무한대 JSON 수정 전후를 웹 소비자 인계 과제2개·4회로 비교한다.
양쪽 모두 지정 CLI를 한 번 쓰고 원본 출력에서만 보고서를 만들어야 한다.
일반 숫자 대조군도 포함하고, 출력 복구는 허용하되 원본·오류 근거를 보존한다.
둘 모두 토큰과 시간이 줄어야 이 좁은 관찰을 채택하며 전체8개 절감률로 쓰지 않는다.
