# Empty mutant checks are incomplete — 2026-09-21

Parent resource: `bd238f1`. Author regression controls, not a model benchmark.

## Reproduction and correction

The helper already returned check exit 5 when unittest executed zero non-skipped
tests. Pytest also returns 5 for no collected tests. The audit-level stop condition
handled these exits only on correct code: a faulty copy could therefore receive
`status: observed`, skip conditional stronger probes, and let a batch continue.
That status was not itself a claim of a killed fault, but it contradicted the
documented incomplete-evidence contract and could mislead downstream consumers.

`tests/test_audit_mutant_empty.py` exercises actual child processes, not mocked
exit statuses. Before the production edit, four test methods produced five
assertion failures (`observed` instead of `incomplete`):

- Unittest mutant skips every test while correct code executes one.
- Unittest mutant's `load_tests` returns an empty suite.
- Stronger native probe runs on correct code but skips on the mutant.
- Pytest mutant removes the only collected test.
- Two-fault batch proceeds beyond the first empty mutant.

The stop condition now reserves exit 5 as incomplete in either variant and phase.
It preserves original check output/exits and stops before conditional skipping or
later batch faults. Explicit inline `SystemExit(5)` is also conservatively
incomplete. This does not classify every runner error, all pytest skips, hostile
early exits or every nonzero status; actual assertions and counts still matter.

Python3.11.16 with installed pytest: all four new test methods pass (0.772s).
Python3.9.6: three pass, pytest control skipped because pytest is not installed
(four discovered, 0.457s). These durations are validation logs, not speed claims.
Single-audit controls check selected bytes and scratch removal; batch verifies
only two child executions and no later audit, plus scratch removal.

Full-checkout follow-up at `31b1479`: Python3.11.16 ran all **1,023 tests in
174.348s**, no failures or skips (`python -B -m unittest discover -s tests`).
This includes the prior Receipt selected-read correction and the new plan-audit
fixture/runner tests. Repository validation, skill quick validation, localized
featured-sync check and whitespace check pass. This is local checkout validation,
not a source-archive rerun, hosted CI success, model benchmark or release approval.

## Separate invocation finding

Code inspection confirms the helper launches Python `-B -c` and calls
`unittest.main(module=None, exit=False)`. It does not provide the exact
`python -B -m unittest` invocation required by the frozen plan-audit tasks.
The guide and both README capability descriptions now disclose this limitation.
The guide advises project facilities for that requirement; no startup adapter
was added, and no old fixture or measured session was changed.

This mismatch does not prove why model sessions chose not to use the helper.
The native-module support in Receipt is a separate implementation, not evidence
that Con Artist supports it. Model cost impact is unmeasured. Featured data and
charts remain tied to their original evidence.

한국어: 결함 복사본에서 테스트가 사라지거나 모두 건너뛰어져도 감사가 완료된
것처럼 처리되는 오류를 실제 실행으로 재현하고 고쳤다. 정상·결함 양쪽의 종료
코드 5를 검증 불완전으로 처리하며, 추가 검증을 생략한 성공이나 탐지로 세지
않는다. 정확한 `python -m unittest` 방식의 미지원도 두 언어에 명시했다.
모델의 도구 미사용 이유나 토큰·시간 절감을 입증한 결과는 아니다.
