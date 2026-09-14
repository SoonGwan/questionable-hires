# Checkpoint 09 form controls — 2026-09-14

Partial review of launch `3a7d972`, resources `9071a1c`;
[intake and whole-run costs](BUNDLE-CONTRACT-09-INTAKE.md).
This covers only pending-form artifacts, not all eight skills or the completed
checkpoint review. No new model sessions were run.

## Contract-sensitive tests, with an original evidence gap

Both retained implementations have per-instance pending state, a duplicate guard,
and `finally` cleanup. Baseline retains seven tests; skill six, plus the copied
ControlledCall asset (byte-identical to the frozen skill). Original requirements
are unchanged. No unrelated retained project files appear in either form cell.

The contract forbids another save during pending, but specifies no return value
for that suppressed duplicate. Baseline's test additionally requires three None
results. Its final implementation passes, but changing only the suppressed return
to False produces `[False, False, False] != [None, None, None]`. This is a false
positive on a contract-valid alternative, not an implementation failure.
Skill's unchanged tests accept the corresponding False alternative.

The original baseline command captures seven passing test results. Original skill
item 8 captures final diff/status but no native test names/count/summary. Despite
that gap, its final answer says all six passed. Do not treat later passing author
replay as original evidence or mark this whole skill session fully verified.

## Separate native replay

[Replay script](replay_bundle_contract_09_form.py) runs unchanged retained tests
in disposable copies under the local run directory, replacing only form.py.
It uses the correct discovery roots (`.` baseline, `tests` skill), explicit native
counts and a 20-second outer deadline. No retained workspace is edited. The
[complete report](results/bundle-contract-09-form-controls/author-replay.json)
includes source inventories, original retained sources, replacement implementations,
commands, full outputs and unsuccessful contract expectations.

| Implementation | Baseline: 7 tests | Skill: 6 tests |
| --- | --- | --- |
| Retained final | Pass | Pass |
| Original missing state | Fail: missing pending and duplicate-value assertion | Fail: missing pending |
| Duplicate guard removed | Fail on extra callback return values | Fail at owned duplicate wait deadline |
| Cleanup removed | Fail: pending remains true | Fail: pending remains true |
| Valid duplicate returns False | **False positive** | Pass |

All ten runs finish before the outer timeout with the expected seven/six discovered
tests. Nine contract expectations match; the baseline valid-alternative expectation
remains false in the report. Removing the skill guard reaches its one-second
owned wait (`asyncio.exceptions.TimeoutError`), not its later callback-count
assertion. Do not describe that as a direct count assertion or a harness setup
failure. Original variants fail on the actual absent pending API. Cleanup variants
reach explicit True-is-not-False assertions. Original test/support bytes remain
unchanged in every copy; retained project inventories match after replay.

Costs remain 66,691 tokens / 82.211s baseline, 96,674 / 73.413s skill. Different
test strategies, seven versus six methods, a valid-alternative false positive,
and the skill's missing original output prevent an equal-work efficiency claim.
This narrow retained-artifact benefit does not establish a general performance
gain or remove the remaining checkpoint review obligations. Charts are unchanged.

## 한국어

폼 과제의 실제 보존 테스트를 별도 복사본에서 검증했다. 두 구현 모두 정상
동작하지만 기본 모델 테스트는 명세에 없는 중복 호출의 None 반환을 요구했다.
같은 계약을 만족하는 False 반환 구현을 잘못 실패시켰고 스킬 테스트는 통과했다.
두 테스트 모두 중복 실행 방지·상태 해제 결함은 검출했다. 스킬의 중복 방지
결함 검출은 호출 횟수 단언이 아니라 소유한 작업의 1초 대기 제한에서 발생했다.

총 10회 재실행 중 9개 계약 기대가 일치했고 기본 모델의 오탐은 그대로 남겼다.
원본은 수정하지 않았다. 스킬 원본 실행에는 테스트 출력이 빠져 있으므로
후속 통과 결과로 이를 보완하지 않는다. 기본 66,691토큰, 스킬 96,674토큰으로
이 과제의 토큰 증가도 그대로다. 전체 평가 검토와 성능 목표는 아직 미완료다.
