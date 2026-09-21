# Existing-file probe transfer01: selection before native outcomes

Selected2026-09-21 at resource`aed8a27`. New exact probe edits are optional;
this experiment must not require their use or remove native verification work.
No model calls have been made for this selection.

Use the already archived pypa/packaging24.2 subset, commit
`d8e3b31b734926ebbcaff654279f6855a73e052f`, from
`packaging-specifier-01-source.json`. Keep its licenses and runtime dependencies.
This reuses upstream source seen in an earlier experiment, not an independent
holdout, newly reported upstream defect or a claim about the latest release.
The earlier experiment audited three comparison operators against the full suite;
this experiment asks to improve one existing constructor smoke test at its path.

## Fixed work and two sizes

Select the first `TestSpecifier` method in source order, `test_specifiers_valid`.
It constructs a Specifier for every entry in `SPECIFIERS`. Investigate whether this
selected test protects string representation, replacing only the return expression
of `Specifier.__str__` with an empty string in the faulty copy. If it survives,
strengthen the existing method to verify each supplied specifier's unchanged string
representation. Keep the constructor check, parameterization, imports and other
file contents. Verify original/stronger tests on correct/faulty implementations.
This is an explicitly scoped stronger contract, not a claim that an upstream
constructor-only test was intended to cover serialization.

Two requests have the same test method, parameter inputs, production package and
assertion obligation. Only the size of the selected test file differs:

- Full: original `tests/test_specifiers.py` (30,731 UTF-8 bytes).
- Prefix control: its exact source prefix through the first method's end line;
  this author-selected subset excludes later tests, without generated padding or
  expensive setup. Label it a subset, not the full unchanged upstream file.

Native pytest selector for every phase:
`tests/test_specifiers.py::TestSpecifier::test_specifiers_valid -q --tb=short -p no:cacheprovider`.
Do not claim that the full upstream suite misses the mutant; unselected later
tests explicitly exercise string representation. Each requested phase must preserve
the same selected parameter cases and identify actual assertion values/status.
Setup/import failures are incomplete, not mutation detection. Source binding must
be verified in the actual native process; the environment also has installed
packaging. Preserve original source/tests/licenses, modes, Git state and installed
skills; only disposable project-local checks are authorized, without installs,
network, publication or permanent production/test edits.

## Preflight and later schedule

Before models, use the existing audit helper to exercise both full-replacement
and exact-edit forms on both sizes; retain native output, copied imports,
preservation and generated-byte equivalence. Fresh-import the public package with
the same interpreter/source roots. Confirm deliberate assertion failures are
behavioral rather than setup errors. Freeze any needed fixture corrections before
launch; never edit a measured fixture.

The intended bounded model comparison is two tasks with no-skill, predecessor
`23f06d2`, and current`aed8a27`: six cells, Astra/medium, one each, serial balanced
order. Prepare and commit exact inputs, settings and schedule before launching;
this selection alone does not start them. Use existing `run.py` controls, not a
new profiler. All attempts and adverse results remain. No forced helper adoption,
favorable retry, speed claim from JSON size alone or featured-chart promotion.

Compare correctness/scope, native work, original token counters and elapsed time.
If the model bypasses the helper, report it; a smaller optional API is not proof
that it saved model work. The small-file control may show no benefit or regression.
This is an operating-range development screen, not broad20–30% generalization.

한국어: 실제 upstream 테스트 파일의 첫 생성자 검사에 문자열 표현 검증을 추가하는
명시적 과제다. 전체 파일과 해당 메서드까지의 짧은 원본 구간을 비교한다. 전체
upstream 테스트의 결함 탐지력을 평가하는 것이 아니며, 도우미 사용을 강제하거나
JSON 길이 감소를 모델 성능 향상으로 계산하지 않는다.
