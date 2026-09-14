# Checkpoint 09 boundary/formatter review — 2026-09-14

Launch `3a7d972`, resources `9071a1c`;
[whole-run intake](BUNDLE-CONTRACT-09-INTAKE.md). Partial pair review, not the
completed whole-bundle evaluation. Historical and featured graphs stay unchanged.

## Boundary fix

Both original traces show the added exactly-18 regression before the production
edit: three discovered tests, exactly-18 False-is-not-True failure, and passing
17/19 neighbors. After the `>` to `>=` edit, the same three tests pass. Native
identities, assertion and counts are captured in both arms. Both final commands
use `&&` to retain a failure before Git review. Resulting production and test
files are byte-identical between arms; no extra retained files.

[Author replay](replay_bundle_contract_09_boundary.py) uses unchanged retained
tests in disposable project-local copies, with bytecode disabled and a 20-second
process bound. It replaces only eligibility.py with final, original, an overly
permissive `>= 17`, or an overly restrictive `== 18` implementation.
[All eight controls](results/bundle-contract-09-boundary-controls/author-replay.json)
match: three discovered tests each; final passes, and each defect reaches the
relevant actual value assertion. Tests and retained project inventories stay
unchanged. These controls do not establish behavior outside those inputs.

Baseline: 80,064 tokens / 60.289s; Receipt: 84,448 / 33.998s. Same retained result
and core before/after evidence, but skill adds entry context, an extra revision
query and installed-file inventory. Receipt reads no comparison helper. Higher
tokens and lower recorded time are both retained, without causal attribution.

## Formatter review

Both inspect the complete three-file project, the single USD call site and the
explicit exclusion of dynamic configuration/third-party formatters. Both recommend
a named format_usd function keeping the exact formatting expression and the
total_label caller API, explaining the removed mutable registry and string lookup.
Their source-based recommendations preserve the stated scope; neither implements
the proposal. All three original files match frozen inputs, with no additions.

Landlord makes two shell calls and explicitly labels verification static. Baseline
makes four and additionally compares the current consumer with the proposed pure
function in memory on seven zero/positive/negative values. Its seven values and
assertion program are captured. The skill does not claim it executed this test.
Baseline's extra probe is not identical work, and these few values would not
establish a universal numerical equivalence claim on their own.

Baseline: 79,963 tokens / 34.641s; Landlord: 49,637 / 28.970s. The lower cost is
associated with a narrower, explicitly static review—not proof of faster execution
of the same probe. No runtime unknown requiring that probe was found in the
supplied fixed-expression contract. This remains an exposed single pair.

The skill answer contains one malformed absolute local link. Full-run export
must remove that private path too, not merely replace exact workspace strings or
the standard `/var/folders/` pattern. This is a publication task still pending,
not a defect in the proposed formatter behavior.

## 한국어

경계값 수정은 두 모델의 최종 코드·테스트가 동일하고, 원본의 수정 전 실패와
수정 후 통과도 확인됐다. 별도 8회 대조는 정상 수정과 18 제외·17 허용·19 제외
결함을 모두 구분했다. 스킬은 토큰이 더 들고 시간은 짧았으며 원인은 단정하지
않는다.

포매터는 두 모델 모두 계약에 맞는 단순화를 제안하고 원본을 보존했다. 스킬은
정적 검토라고 명시했고 기본 모델은 7개 값의 추가 실행 검증을 했다. 비용
차이에 작업량 차이가 있어 같은 검증을 더 빠르게 했다는 뜻은 아니다. 스킬
답변의 잘못된 로컬 링크도 전체 결과 공개 전에 가려야 한다. 남은 과제 검토와
공개본 대조는 계속 필요하다.
