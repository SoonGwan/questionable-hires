# Hostage input-contract candidate 01 — 2026-09-21

**Not adopted or performance-validated.** Base resource `6516f5e`; transformation
in `hostage_input_candidate.py`. Only the observable-contract paragraph changes.
Discovery, async ownership/cleanup, native verification, scope and stop rules stay
unchanged. No helper, extra reference, mandatory mutation tool or test quota is added.

The [retained-suite replay](HOSTAGE-COVERAGE-REPLAY-01.md) showed a concrete blind
spot: string-only keys did not distinguish unintended argument conversion. The
candidate explicitly covers arguments as well as results and asks for values that
distinguish plausible contract violations. Identity is conditional on the actual
contract; required normalization must use value assertions instead. This avoids
turning one missed pass-through fault into a universal identity requirement.

Construction tests verify exactly one paragraph is replaced and reject absent,
duplicated or already-applied input. These tests **do not** demonstrate behavioral
quality, lower token cost or safer model decisions. Production skill bytes remain
unchanged while the candidate awaits behavioral comparison.

## Next evaluation requirements

Use a different small implementation task with an explicit opaque argument
passthrough contract, plus a matched task explicitly requiring normalization.
Supply all scored obligations to every condition; do not reveal expected fixes.
Preflight real healthy and deliberately defective controls before freezing.
Compare no-skill, original and candidate in fresh sessions on at most two tasks;
retain all outcomes, repairs, native verification and input/output/time costs.
Review application behavior and whether generated assertions discriminate the
specified contract. Test-method count is not a success criterion.

Do not reuse the exposed refresh-owner task for selection, lower scope/coverage to
save tokens, punish permitted normalization, or adopt based solely on one favorable
pair. If the extra paragraph does not help or increases cost without useful gains,
retain that result and reject or reconsider the candidate instead of quietly
replacing attempts. There are no new model results at this checkpoint.

한국어: 전달 계약을 구별할 입력 선택을 명시하는 한 문단 후보를 만들었다.
객체 동일성은 계약이 요구할 때만 검사하고, 정규화가 요구되면 그 값을 검증하도록
구분했다. 아직 실제 스킬에는 적용하지 않았으며 문장 교체 검사만으로 성능 개선을
주장하지 않는다. 별도 두 과제에서 무스킬·기존·후보를 비교한 뒤 채택을 판단한다.
