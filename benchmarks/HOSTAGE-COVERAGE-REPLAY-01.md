# Hostage coverage replay 01 — 2026-09-21, parent `7d80f48`

This is **post-run author analysis**, not a model experiment or improvement claim.
It uses the unchanged final artifacts from screen03 (`ee5eb28` resources), whose
baseline/current sessions remain frozen. No production skill was changed here.

Reproduce: `python3 -B benchmarks/check_hostage_coverage.py`.
[Retained native output and source hashes](hostage-coverage-replay-01.json)
identify both generated test suites and the copied current support asset.
The final `preview.py` implementation is byte-identical between conditions.
Copies run project-local with a 15-second process bound; originals are not edited.
One regression test exercises all ten actual native runs in 0.995s on Python3.11.

## Test count is not coverage

| Applied implementation | Baseline suite (5 methods) | Skill suite (8 methods) |
|---|---|---|
| Unchanged healthy implementation | Pass | Pass |
| Older request can publish its result | Assertion failure | Assertion failure |
| Older request can clear pending | Assertion failure | Assertion failure |
| Starting refresh discards previous value | Assertion failure | Assertion failure |
| `fetch(key)` becomes `fetch(str(key))` | Assertion failure | **Pass: not detected** |

Every observed rejection is a real assertion failure, not a timeout, import error
or test discovery failure. Both suites execute all their native methods. Baseline
uses subtests for some separate scenarios, so 5 versus 8 does not establish less
work or missing transition coverage. These four authored mutants are not an
exhaustive audit or a general ranking of the suites.

The last mutation violates the supplied `fetch(key)` passthrough by converting the
argument. Baseline uses object-valued keys and checks the actual argument identity.
The skill suite uses string keys and verifies argument equality; string conversion
is indistinguishable for those chosen values. This is an input-domain blind spot,
not a defect in the controlled callback asset. Do not impose object identity where
the application's contract permits normalization or only promises value equality.

Screen03 recorded 131,015 skill tokens versus 87,521 baseline, with different
test constructions and both meeting the original reviewed criteria. The replay
does not rescore those criteria, rerun their models or prove which instruction
caused this difference. It rejects an unsupported optimization: simply removing
the additional three methods or labeling the larger suite more thorough.

## Next improvement boundary

Prioritize contract-discriminating inputs and reuse of covered transitions over
method count. Evaluate that on a different task with an explicit callback argument
contract and a control where normalization is permitted; do not retrofit new
criteria onto screen03 or tune repeatedly on this exposed refresh task. Preserve
existing cancellation, cleanup, result/error and ownership checks. Any new skill
candidate must still show whole-task token/time cost against no-skill work, not
claim a mutation-replay pass as model efficiency.

한국어: 기존 모델이 작성한 테스트를 그대로 두고 같은 코드 결함을 넣어 비교했다.
상태 소유권 관련 세 결함은 양쪽이 모두 잡았지만, 인자를 문자열로 바꾸는 결함은
문자열만 입력한 스킬 쪽 테스트가 놓쳤다. 테스트 개수보다 계약을 구별할 입력이
중요하다는 단서이며, 스킬 전체 우열이나 성능 향상 결과는 아니다. 기존 모델
실행·점수는 보존하고 다음 후보는 별도 과제에서 검증한다.
