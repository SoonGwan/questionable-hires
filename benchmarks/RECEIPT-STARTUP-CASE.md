# Receipt native startup transfer — 2026-09-20

New authored compatibility probe; **no model run or performance result yet**.
The support-routing candidate from `receipt_route_candidate.py` remains isolated.
The preceding [routing screen](results/receipt-route-01/README.md) covered routine
SQLite comparison only, not a required project startup configuration.

`receipt_startup_case.py` supplies a committed CSV parser fix with five current
native tests. `sitecustomize.py` initializes the delimiter from `format.json`.
The documented runner explicitly enables the copy-local hook with `PYTHONPATH=.`.
Tests require the hook to have run **before test import**, report implementation
and hook paths with the native PID, and call the actual parser. They cannot
silently initialize startup themselves and then call that native startup proof.

The task explicitly requires identical current tests/hook/configuration for both
revisions, actual defect assertions, all controls, full revisions, same-process
imports, preservation of originals/ignored cache/notes and deletion of owned
copies. It does not authorize repairs or replacement of startup behavior.
Valid single records, quoting, doubled quotes, empty fields and Unicode are
specified; malformed/multiline input and alternate delimiters are out of scope.

Preflight in `tests/test_receipt_startup_case.py` checks actual native outcomes:

- Before: two quoted-field assertion failures, three passing controls.
- After: all five tests pass with unchanged startup/configuration.
- Deliberate `-S`: RuntimeError identifying missing startup before test import,
  not five executed tests or defect-specific list assertions.
- Existing Receipt helper: rejects project-local startup replacement, preserving
  originals and cleaning scratch. This is incompatibility, not bug reproduction.

Both local tests pass on the system interpreter. During authoring, an overly
specific expectation for unittest's formatting of the deliberately disabled
startup was corrected: module-import RuntimeError escapes as a traceback rather
than `FAILED (errors=1)`. The test now checks the actual setup error and absence
of five-test/defect evidence. No model attempt was made or discarded.

The next frozen comparison should use fresh no-skill, original `ca668a4` and
unchanged routing-candidate sessions. There is no requirement to use the helper:
preserving the native runner is correct here. Review whether the agent recognizes
the compatibility boundary and uses valid native isolation; an honest unresolved
result is preferable to false verification but is not full task completion when
the documented runner can complete it. Preserve attempts and cost. A single
authored task does not establish general performance or safety; do not combine
its cost with historical baseline sessions as if simultaneously controlled.

한국어: 프로젝트 시작 설정이 필요한 CSV 검증 과제를 추가했다. 실제 검사로
수정 전 오류 2개·수정 후 5개 통과를 확인했고, 시작 설정 생략은 다른 실행
오류로 구분된다. 기존 도우미가 이 설정을 대체하지 않고 거부하는 것도 확인했다.
스킬이 올바른 프로젝트 실행 방식을 선택하는지 보기 위한 과제이며, 모델 성능은
아직 측정하지 않았다. 후보 채택이나 배포 준비 완료를 뜻하지 않는다.
