# Receipt: preserve native pytest collection and failure evidence

2026-09-15, parent `99c25be`. Reliability correction, **not measured model savings**.

The [real HTTPX preflight](HTTPX-RECEIPT-JSON-01.md) exposed a defect: Receipt
imported listed test modules before pytest installed assertion rewriting and
before project configuration hooks ran. Failing checks could lose actual values,
or fail during premature loading instead of exercising the intended behavior.

## Change

The pytest bootstrap now uses the documented
[in-process pytest entry point with a plugin](https://docs.pytest.org/en/stable/how-to/usage.html#calling-pytest-from-python-code).
Native configuration and collection load tests first; a collection-finish hook
verifies the listed module paths inside that same comparison process before test
bodies execute. It does not infer test modules from names, force rewriting, edit
assertions or replace project hooks. Unittest and native-module startup remain
unchanged. Verification errors stop with check 7; a 0/1 return without reaching
verification is incomplete, not an observed comparison.

Collection/plugins can execute before verification. This remains a trusted-test
tool, not a sandbox or proof that every requested assertion ran. Native collection
failures retain pytest's own exit behavior. Collect-only and skipped results still
require coverage inspection. Documentation describes these boundaries.

## Actual regression and controls

[Seven new native tests](../tests/test_receipt_pytest_loading.py) ran on the old
helper first: **four failed, three passed** in 1.274 seconds. Old failures were
missing `19 == 18` details (direct and whole-comparison paths), configuration-hook
ordering, and treating `--version` as a verified comparison. No mocks of pytest.

After the correction, the identical seven passed in 2.225 seconds:

- Configured `checks_*.py` collection retains actual `assert 19 == 18`; changing
  only implementation value to 18 passes both original native assertions.
- The original project configuration hook runs before test-module import.
- Explicit plain-assert mode remains plain.
- An escaped standard-library import and an import raising `SystemExit(0)` both
  stop before native test bodies, with exit 7 and decisive error output.
- No-session `--version` cannot claim completed import verification.
- Whole comparison preserves original bytes/modes and Git status, with owned
  comparison copies removed.

The complete Receipt suite, including the new tests, passed **102 tests in
36.348 seconds**, Python 3.9.6 / pytest 8.3.4. These durations are test execution
observations, not before/after speed comparisons.
Installation-related checks also passed (21 tests, 2.604 seconds), along with
skill validation, repository validation, featured-language synchronization check
and whitespace checks.

[Fresh actual HTTPX verification](httpx-receipt-json-02-preflight.json) keeps the
same source revisions, native five tests, support/configuration and verbose
settings as the prior final preflight, now additionally requiring provenance
for `tests.test_content`. Before: four actual failures plus one passing control;
after: five passes. Detailed values survive while test-module provenance is
verified. All 125 original file hashes/modes remain unchanged, copies removed,
no timeouts/truncated output. The artifact records the changed helper SHA-256.
The three earlier preflights remain untouched.

## Interpretation and next work

This fixes demonstrated helper behavior, not overall skill efficiency. No model
session ran here; no headline graph, frozen result or all-eight gain changed.
Next: freeze the real-source model comparison against a specified baseline and
evaluate whole-task success, scope, tokens and time without favorable retries.

한국어: pytest가 테스트를 정상적으로 수집한 뒤 같은 프로세스에서 출처를
확인하도록 수정했다. 실제 실패 값과 프로젝트 설정 순서를 복구했고, 잘못된
출처·조기 종료는 계속 차단한다. 새 검사 7개는 수정 전 4개 실패에서 수정 후
모두 통과로 바뀌었고 Receipt 전체 102개도 통과했다. 실제 HTTPX 원본 테스트와
125개 파일 보존까지 확인했다. 이는 도우미 오류 수정의 증거이며, 모델 토큰·시간
절감이나 8개 스킬 전체의 20–30% 개선을 입증한 결과는 아니다.
