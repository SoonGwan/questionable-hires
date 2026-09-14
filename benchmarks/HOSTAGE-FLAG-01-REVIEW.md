# Flag handoff 01 — durable evidence used in a synchronous task

2026-09-15; [protocol](HOSTAGE-FLAG-01-PROTOCOL.md), launch `094cc69`, resources
`fe3faa8`. Four fresh sessions completed with known usage, no timeout, limit or
retry. Two correlated authored tasks, n=1; not production-user evidence.

| Variant | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| a: faulty parsing | 125,674 / 93.591 | 116,905 / 79.170 |
| b: valid parsing | 120,827 / 83.164 | 116,243 / 72.848 |
| Sum | 246,501 / 176.755 | 233,148 / 152.018 |

Input includes cached input once; add output, not cached input again. Observed
sum reductions: **5.42% tokens / 14.00% elapsed time**. Both pairs decrease, but
work differs. Baseline a runs an additional before-fix check (10 methods, 124
subtest failures), then passes after fixing. Skill a verifies only after fixing.
Baseline b has extra read-only-mapping and process-environment controls; all suites
group cases differently. No causal or general 20–30% gain is established.

## Original behavior and evidence

Both a implementations fix false spellings and invalid input; both b production
files remain unchanged. Caller, requirements, notes and earlier evidence remain
byte-identical. The original two test methods retain the same AST in all cells.
No unrelated async helper is read/copied by the skill sessions.

The two skill sessions read the optional native-evidence reference, execute its
single-run shell recipe, then read argv/output/exit in their final review call.
Each original native report contains eight named tests, `OK` and exit 0. These
are supported handoffs, not prose substituted for missing native output.

Baseline also fulfills the requested retention contract using native subprocess
redirection: a stores both failing and passing runs; b stores one passing run
of 13 methods. The wrapper's own exit 0 on baseline a's failing run is not the
test exit: the retained test exit is 1 and its native failure output is present.
The model reads the failed report's head/tail, then fully reads the passing report.
No requirement to use our recipe was imposed on baseline or skill.

There are five native verification runs across four sessions. Command histories
show each report's original creation/redirection and later inspection. All four
final successful report bodies are contained verbatim in captured read-command
output, including native identity/count and status. Retained command arguments
match `python3 -B -m unittest discover -v`; report paths appear in final handoffs.
This checks original evidence, not an author replay used to fill a gap. No actual
terminal loss occurred in the reviewed final captures, so recovery from a real
CLI omission has not been demonstrated by this model experiment.

## Test review and separate controls

All retained tests call actual `read_flag` and `worker_options`. They exercise
true/false spellings, case/whitespace, both defaults on missing/None, invalid and
blank strings, requested keys, caller return fields, and mapping preservation on
returns/errors. No mocked replacement parser, skipped suite or overridden runner
was found. Baseline b's `patch.dict` isolates a process environment check and is
scoped to its context. No async cleanup is required by these synchronous cases.

[Separate controls](results/hostage-flag-01-controls/author-replay.json), generated
by [the audit/replay program](replay_hostage_flag_01.py), produce 16/16 expected
outcomes. Each retained suite passes final production, fails a truthiness mutant
with relevant false-value/ValueError assertions, and accepts an equivalent valid
implementation with different error wording. The separate frozen five-method
oracle passes each final production. Each run has a 15-second outer bound and
unchanged retained tests/evidence; original projects are unchanged. These finite
checks do not exhaust every string or prove general production readiness.

## Publication and next decision

[All four cells](results/hostage-flag-01/run.json) retain events, commands, answers,
diffs and complete project text including native reports. Raw turn usage matches
metadata; exported events/project text and filename sets reconcile to redacted
originals, source SHA-256 provenance matches, installed resources remain stable.
Home/temp/key-pattern scan finds no matches; not a universal privacy guarantee.

This establishes useful conditional recipe adoption on a new synchronous task,
with modest descriptive cost decreases. Keep this feature, without adding another
rule for every command variation. The whole-eight objective remains open: shift
attention to other hires and known costly workflows rather than keeping this
pair in a favorable-number loop. Prior adverse async results remain linked in
the current status. No featured or historical chart is changed.

## 한국어

새 동기식 과제 4세션에서 양쪽 모두 동작·정상 코드 보존·테스트 기록 전달을
확인했다. 스킬 두 세션은 추가한 선택적 증거 보존 예시를 실제로 사용하고 기록을
읽었다. 기본 모델도 자체 방법으로 기록했다. 최종 성공 로그 4개는 실제 읽기
명령 출력과 일치하며, 원본 대신 재실행 결과를 끼워 넣지 않았다.

합계 토큰 5.42%·시간 14.00% 감소가 관측됐지만 기본 모델의 추가 수정 전 검증과
테스트 범위 차이가 있어 순수한 절감으로 단정하지 않는다. 별도 대조 16회는
예상대로 동작했다. 실제 CLI 출력 누락 복구를 이 실험에서 재현한 것은 아니다.
기능은 유지하되 같은 과제 반복보다 나머지 스킬의 비용·실사용 개선으로 이동한다.
전체 20~30% 목표와 실사용자 검증은 미완료이며 기존 그래프는 유지한다.
