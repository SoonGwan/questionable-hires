# Refresh-owner 01: useful tests, unsupported original pass claims

Reviewed 2026-09-15. [Frozen protocol](HOSTAGE-REFRESH-01-PROTOCOL.md), launch
`3c29443`, measured skill resources `864005b`. All four scheduled Astra medium
sessions completed without timeout, account limit or model retry. Two correlated
authored variants, one observation per arm: not independent production evidence.

## Original observations

| Variant | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| a: faulty pending cleanup | 113,201 / 128.345 | 98,755 / 109.572 |
| b: valid pending cleanup | 108,168 / 122.900 | 99,123 / 120.010 |
| Sum | 221,369 / 251.245 | 197,878 / 229.582 |

Tokens are input (cache already included) plus output, not an additional cache
sum. Observed ratio-of-sums reductions: **10.61% tokens, 8.62% elapsed time**.
No confidence interval, causal claim or accepted whole-task performance win.
Baseline a repaired its cancellation-identity test harness after five native
failures, then ran the five-method suite twice successfully. Work is unequal.

Both arms make the same generation-guard fix in a and leave valid production b
unchanged. Requirements and unrelated notes are byte-identical to frozen input.
Skill helper copies and installed resources are unchanged. Baseline b captures
eight native tests passing with process exit 0.

**Both skill pass claims lack original native evidence.** In a, command item_7
contains only the final diff/status, without native results or its printed exit
marker. In b, item_7 contains the printed test exit 0 and later checks, but no
native test identities/count/results. Both final answers nevertheless claim
eight tests passed. This does not prove tests failed or never ran, but it does
fail the required evidence-grounded report. A shell exit cannot substitute for
the missing transcript. No strict four-of-four success score is claimed.

All four [exported cells](results/hostage-refresh-01/run.json) retain their answers,
commands, events, metadata, diffs and complete retained project text. Raw turn
usage matches metadata; exported events/project text match path-redacted originals;
source SHA-256 provenance matches. Home/temp/token-pattern privacy scan found no
matches. These checks are not proof of universal secret detection.

## Separate author controls

[Replay program](replay_hostage_refresh_01.py) runs unchanged retained suites in
project-local disposable copies with 20-second process bounds. Each arm/variant:

- Final production passes its retained suite (baseline a: 5 methods; others: 8).
- Unconditional pending cleanup fails with actual False-is-not-True assertions,
  not setup errors or timeouts.
- An alternative valid generation increment of two passes: no required internal
  unit increment is invented.
- The separate frozen six-method author oracle passes on final production.

[Second control report](results/hostage-refresh-01-controls/author-replay-02.json):
16/16 expected outcomes, original projects unchanged. This is deliberately narrow:
one faulty owner and one valid alternative are not exhaustive coverage. It cannot
fill either original capture gap or add evidence to the timed run.

The [first report](results/hostage-refresh-01-controls/author-replay.json) is retained:
its checker accepted `assertTrue`'s lowercase `true` but not `assertIs`'s uppercase
`True`, falsely marking two actual intended failures unmatched. The parser now
accepts either native spelling. All 16 controls were rerun, not selected model
cells; original observations and first outputs remain available.

## Candidate correction, not yet model-validated

Replace Hostage's instruction to batch tests with final diff/status with dedicated
native-test commands, and batch only the non-test checks separately. The existing
requirement to inspect native results and safely recover missing evidence stays.
This removes conflicting pressure to combine outputs; it does not establish the
capture mechanism's cause or guarantee capture. No new general-purpose helper,
mandatory report file, dependency, or production behavior change is introduced.

Skill structure validation and two frozen-fixture tests pass (0.172s). These are
local author checks, not proof of model adoption. Next test: fresh prospective
sessions checking whether native evidence is actually retained and inspected,
alongside behavior and cost. Historical/featured charts remain unchanged.

## 한국어

새 동시성 과제 2종 × 기본/스킬 4세션을 모두 보존했다. 합계 기준 토큰
10.61%, 시간 8.62% 감소지만 반복 1회·서로 연관된 과제·작업량 차이가 있고,
스킬 2세션은 원본 테스트 결과 없이 통과를 보고했다. 성공 실적으로 인정하지
않는다. 양쪽 모두 필요한 수정만 하고 정상 구현과 사용자 메모를 보존했다.

별도 복사본 대조에서는 정상 구현·다른 정상 카운터·정답 테스트가 통과하고
잘못된 상태 해제는 실제 단언으로 실패했다. 대조 판독기의 대소문자 오류를
수정한 16회 결과와 첫 결과를 모두 남겼다. 재실행은 원본 증거 누락을 메우지
않는다. 다음 후보는 테스트 실행과 최종 Git 점검을 분리하도록 고쳤다.
구조 검사·로컬 테스트는 통과했지만 모델의 실제 보고 개선은 아직 미검증이다.
기존 그래프나 대표 수치는 바꾸지 않는다.
