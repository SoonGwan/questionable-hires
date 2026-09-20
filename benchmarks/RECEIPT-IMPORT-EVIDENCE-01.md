# Receipt: direct native import evidence

2026-09-20, parent `8647f8a`. This is an implementation/test checkpoint, not a
model-efficiency result. [Prior six-session evidence](results/receipt-selection-01/README.md)
shows both helper-using sessions inspecting implementation after execution;
the original session searches specifically for import/provenance behavior.

The native `Verified copied import:` line now appends JSON containing the resolved
module `path` and process `pid`. Both bootstrap runners and native-module startup
emit this only after the existing copy-local check succeeds. No extra model call,
import-only subprocess, copied report file or automatic discovery is introduced.
Existing assertion output, native exit semantics, cleanup and scope remain intact.

This makes the observed location inspectable from the actual result rather than
requiring readers to infer it from implementation. It records import-time identity,
not code hashes or protection against later monkey-patching. Output remains bounded
to 12,000 characters: truncated evidence is unavailable, not silently reconstructed.
The extra path/PID also adds output tokens; net model cost must be measured.

## Executed controls

- New native identity regression fails against the old helper in both bootstrap
  and module modes: zero detailed identity records instead of one, while the actual
  intended before assertion still fails. The escaped-import negative control passes.
- After the change, actual native unittest checks compare helper identity with
  the module path/PID printed by the test process itself, retain before failure /
  after pass, verify separate copies, original preservation and copy removal.
- Actual pytest collection/test execution checks the same path/PID identity and
  retains a detailed `assert 19 == 18` failure plus passing controls. Existing
  configuration-before-import and assertion-rewriting tests remain passing.
- Python 3.11 with pytest 8.3.4: **109 Receipt tests, all passed, 43.727 seconds**.
  Command: `python -B -m unittest discover -s tests -p 'test_receipt*.py'`.
  The environment is isolated under ignored `benchmarks/local-runs/`; no global
  Python packages or user's model configuration were changed.
- Python 3.9 install checks: **21 passed, 2.714 seconds**. Skill validator and
  featured synchronization check pass. Earlier system-Python run discovered 108
  tests with seven pytest skips before the additional pytest identity test; it is
  not the all-passing coverage claim above. Runner unit-test mock sessions are not
  real model measurements.

No featured chart, frozen comparison input or historical result is changed.
Next model comparison must use new work and retain all attempts; checking fewer
obligations is not efficiency. Other roles remain in the overall performance scope.

한국어: 검증 도우미가 실제 테스트 프로세스에서 불러온 파일 경로와 프로세스 ID를
직접 출력하도록 개선했다. 별도 확인 프로세스가 아닌 실제 테스트의 값과 비교하며,
수정 전 실패·수정 후 통과, 잘못된 외부 import 거부, 원본 보존·정리도 검증했다.
pytest를 포함한 Receipt 검사 109개와 설치 검사 21개가 통과했다. 출력량은 조금
늘므로 토큰 절감을 보장하지 않는다. 다음 모델 실험에서 실제 확인 작업이 줄어드는지
측정해야 하며, 대표 그래프와 기존 측정값은 그대로 유지한다.
