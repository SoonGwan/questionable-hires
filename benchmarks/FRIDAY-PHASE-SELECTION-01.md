# Friday phase-specific consumers — 2026-09-15 KST

Parent `761a4b8`. This is a local capability check, not a model benchmark or a
claimed explanation for checkpoint 09's higher Friday cost. That model used
native SQLite without loading this helper.

The optional SQLite matrix previously ran every declared reader after every
phase. An explicitly scoped `checks` list on a phase now permits the documented
active consumers to differ between deployment and rollback states. Omission
preserves the prior all-readers behavior and output. Changed selections/orders
are recorded as `selected_checks`; unselected readers have no observations and
are not certified. All declared source/query inputs still undergo preparation
and the existing budgets; this does not expand accepted input sizes.

`tests/test_friday_matrix.py` runs real SQLite through initial old schema, renamed
new schema with an update, and rollback. The trace contains exactly the three
selected SELECTs; returned values are 1, 2, 2, proving fresh post-write and
post-rollback observations rather than cached results. Activating the old reader
during the new schema produces the actual missing-column error. Selection is
therefore a contract choice, not an automatic way to hide failed checks.

Other controls reject unknown/duplicate/empty/non-list/non-string selections
before database creation, compare explicit-all output to the unchanged default,
and retain write denial with reordered consumers. All **39 matrix tests pass in
0.398s** (native unittest summary, exit 0). No test claims a SQL query count
reduction proves equal-work model efficiency; no original benchmark is rescored.

## 한국어

배포 단계별로 실제 활성 조회 코드를 선택할 수 있도록 Friday의 선택형 SQLite
도우미를 확장했다. 지정하지 않으면 기존처럼 전체 조회를 실행한다. 선택하지
않은 조회는 통과가 아니라 미실행이며, 실제 롤아웃·롤백 요구사항에 따라 선택해야
한다. 기존 소비자가 여전히 활성 상태라면 검사에서 빼면 안 된다.

실제 SQLite 실행에서 초기 값 1 → 새 버전 쓰기 후 2 → 롤백 후 2를 확인했다.
새 스키마에서 구버전 조회를 활성화한 대조군은 실제 컬럼 오류를 냈다. 관련
테스트 39개가 통과했지만, 모델의 사용 여부와 토큰·시간 절감은 아직 측정하지
않았다. 기존 그래프 수치는 변경하지 않는다.
