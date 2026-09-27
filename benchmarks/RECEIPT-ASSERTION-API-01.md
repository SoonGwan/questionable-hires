# Receipt assertion observation API01

Historical pre-model functionality checkpoint; subsequent [original model review](RECEIPT-ASSERTION-API-01-REVIEW.md) reports tokens+25.03%,time−5.05%,no efficiency adoption.

2026-09-27; implementation parent `60ced61d`. Local opt-in candidate,
**zero model runs**. No whole-task token/time, all-eight improvement, full release,
remote installation or hosted delivery claim. Previous adverse
[optional-detail01](RECEIPT-OPTIONAL-DETAIL-01-REVIEW.md) remains declined;
its hand-written observer failures motivated this separate mechanism.

## Contract

Recipe `observe_assertions: true` is unittest-only in both bootstrap and module
modes. Default off does not load the observer or add a result field. The new
`assertion_observation` records standard current-thread `assertEqual`/`assertIsNot`
primitive argument pairs; first/second arguments are named actual/expected,
without inferring developer intent. Native assertions execute unchanged.
Reports are bounded to4096 bytes/64 records with bounded primitive traversal.
No arbitrary repr callbacks, full assertion coverage or other-thread observation.

Existing hooks are never replaced. Unavailable values, observer errors, missing
or oversized sidecars, no selected calls, budget exhaustion or hook replacement
mean incomplete observation: check7, comparison incomplete/CLI2, no later version.
Actual native exit and suite counts remain available. Complete observations do
not establish a repair without native before-failure/after-pass evidence.

## Executed local checks

- `python3 -B -m unittest discover -s tests -p test_receipt_assertion_observation.py -v`:
  six tests pass. Both native modes run unchanged six-test fixtures with actual
  before exit1/after0 and seven observed argument records; exact source inventory
  and owned-copy cleanup pass. Default, invalid options, existing hook, controlled
  encoder failure and oversized report controls pass. Incomplete cases stop after
  before while preserving its native failure. The original command output was
  unavailable after context truncation; the recorded six-test result is a fresh
  local execution, not recovered original evidence or a model retry.
- Native invocation regression tests:17 pass (including intentional configured
  hook error diagnostic); multiple-before tests:7 pass.
- Temporary Receipt-only installation matches checkout bytes/modes, including
  `assertions.py`. Installed helper executes both modes against the reused local
  fixture: four native six-test processes, before1/after0, complete observation,
  originals unchanged and scratch removed. Owned installation removed on exit.

These authored/reused fixtures are local functionality evidence, not independent
model validation. Prototype boundary/ownership evidence remains separately dated
in [prototype02](ASSERTION-OBSERVER-PROTOTYPE-02.md) and
[native prototype01](ASSERTION-OBSERVER-NATIVE-PROTOTYPE-01.md); neither measures
this API's stopping contract or token savings. No paid repeat is implied here.

## Measured resource identity

| File | SHA256 |
| --- | --- |
| `skills/receipt/scripts/compare.py` | `665ed70befc5ed014874b58f8a8e59696161e0baee443c55dfff2c910f288cfc` |
| `skills/receipt/scripts/assertions.py` | `31884519110b4547d34f11d62011a34053ba0b86a40e4f194b667112a1967806` |
| `skills/receipt/references/existing-fix.md` | `928c86f52294f2a256c3cda6f789fda325de59cd54373dd4edf7cf6b051eb55f` |
| `tests/test_receipt_assertion_observation.py` | `63e027b6b78ee324359139cf9b15fe4a6d85733e7221c3a134eeb040753e2d99` |

한국어: 실제 단언 인자를 확인해야 할 때만 켜는 후보 기능이다. 관찰에 실패하면
원래 네이티브 결과를 보존하고 비교를 미완료로 중단한다. 로컬 검사와 임시 설치는
통과했지만 모델 토큰·시간 절감이나 전체8개 개선은 아직 측정하지 않았다.
