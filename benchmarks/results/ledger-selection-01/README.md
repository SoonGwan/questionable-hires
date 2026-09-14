# Ledger selection screen 01 — reviewed 2026-09-15

**Same requested behavior, fewer recorded tokens but slower skill execution.**
The new helper batching capability was not exercised, so this result does not
measure that feature's effect. Both agents chose native Python orchestration.
Launch `dde6b61`, skill resources `f9844ad`, Astra medium, one task × two arms ×
one repeat, serial, persisted sessions, no retries/exclusions/timeouts.

| Resource | Baseline | Skill | Skill change |
| --- | ---: | ---: | ---: |
| Input + output tokens, cache included once | 70,374 | 57,922 | −17.69% |
| Full CLI wall time | 52.059 s | 56.767 s | +9.04% |
| Required native test processes | 6 | 6 | Same |

See [frozen protocol](../../LEDGER-SELECTION-01-PROTOCOL.md),
[cases](../../ledger-selection-01-cases.json), [run manifest](run.json) and
[metadata](summary.json). The fixture is authored and intentionally relevant to
the supported selection boundary, not an independent real-repository holdout.
n=1, shared host/cache and different orchestration prevent causal attribution.
No overall 20–30% gain or featured-chart change follows.

## Reviewed native evidence

| Method | Normal exit, both arms | Faulty exit, both arms | What the check establishes |
| --- | ---: | ---: | --- |
| `test_rejects_missing_destination` | 0 | 0 | The expected exception/message still occurs; no persisted-balance check |
| `test_error_keeps_persisted_balances` | 0 | 1 | New connection reads actual `a=90` versus expected `a=100` after failure |
| `test_success_moves_balance` | 0 | 0 | Successful transfer persists `a=90, b=30`; error handler is not reached |

Each arm runs exactly six native unittest processes, one test per process; no
grouped suite or stronger probe. The mutant changes only the error handler's
rollback into commit and preserves the re-raise. The failed assertion at test
line 28 reports the concrete persisted rows, not a setup exception. Both final
answers accurately explain the uncompensated debit and coverage limits.

[Baseline commands](ledger-test-selection--baseline--1/commands.json) use a native
Python script with an 8-second deadline per child. [Skill commands](ledger-test-selection--skill--1/commands.json)
use a similar script with 20-second deadlines and `-E -s` interpreter flags.
Both use Python 3.9.6, the same unchanged tests and inputs within each arm, and
copy-local native test imports. Actual check outputs identify the disposable test
paths. These launch details differ across arms and are disclosed, not normalized
away. The helper and its guides are never invoked/read in the skill trace.

The skill batches discovery/source reads into one outer tool call and execution
into another; baseline uses three outer calls. Each arm has three completed shell
commands. This is an observed orchestration difference, not an isolated explanation
for resource differences. It does not justify forcing helper use in simple audits.

## Capture and integrity

Reviewed stored tool records supplement CLI events for both arms:
[baseline](ledger-test-selection--baseline--1/tool-records.json),
[skill](ledger-test-selection--skill--1/tool-records.json). Every selected call has
its matching output; neither has duplicate/unmatched call IDs. The native execution
response contains all six `Ran 1 test` summaries and the single real failure in
each arm. No author replay supplies these outcomes. Full rollout context remains
local; exported excerpts retain source hashes and original record line numbers.

All three supplied project files are byte-identical after each run and no project
scratch remains in the retained snapshots. Original logs report cleanup; baseline
checks all three original files itself, skill checks the two Python files and the
author independently verifies AGENTS.md too. Installed skill resources remain
unchanged. Raw CLI streams equal exported events after path redaction; artifact
hashes reconcile. These checks do not establish whole-filesystem race protection.

## Decision

Keep this mixed result and the optional batching capability provisionally. The
screen validates native routing and scoped audit execution, not the new API's
whole-task value. Do not repeat this task to chase a favorable time result or
force helper use. Further work should address a genuinely helper-relevant workflow
where repeated setup is necessary; require equal work and retained responses in
every comparison arm. Broad performance remains unproven.

한국어: 양쪽 모두 동일한 여섯 검증을 정확히 수행했다. 스킬 토큰은 17.69% 적었지만
시간은 9.04% 더 걸렸다. 새 일괄 제출 기능을 사용하지 않았으므로 그 기능의 효과로
해석할 수 없다. 실제 실패·각 종료 코드·원본 보존·정리를 확인했고 양쪽 도구 응답도
보존했다. 단일 작성 과제·각 1회 결과이며 전체 성능 개선이나 대표 그래프 변경의
근거로 쓰지 않는다. 도우미 사용을 강제하거나 같은 과제를 유리해질 때까지 반복하지 않는다.
