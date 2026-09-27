# Receipt path observation candidate — 2026-09-27

Parent `35342e9c`. Unpromoted candidate; ordinary skills remain at the measured
integration06 resource `1d0e92ac`. [Integration06 protocol](ALL-EIGHT-CURRENT-06-PROTOCOL.md).

The original current `ledger-delivery-b` cell requested `observe_assertions:true`.
Its before suite ran five tests with the expected two retry failures, but five
`assertEqual(Path(...).parent, ROOT)` setup checks could not be represented by the
primitive-only observer. It returned `reason:unavailable_value`, retained native
exit1 and reported incomplete check7. The model then ran the entire comparison
again with observation disabled. This is an observed extra execution; it does
not establish that all of the token difference is caused by this limitation.

[Candidate transform](receipt_path_observation_candidate.py) supports exact standard
`PosixPath`, `WindowsPath`, `PurePosixPath` and `PureWindowsPath` values as typed
lexical strings. No resolving, file reads, arbitrary object representation or
subclass conversion is added. Path text is bounded to 256 characters; existing
node, container, record and report-byte bounds remain. Format v3 distinguishes
the added typed values from v2. Unknown values still make observation incomplete;
native assertions and failure exits are preserved.

[Native controls](../tests/test_receipt_path_observation_candidate.py) cover typed
values, bounds, custom subclasses, genuine assertion failure, profile cleanup,
and the same complete/partial SQLite fixes in both invocation modes. The SQLite
control compares the original incomplete observation with the candidate while
retaining required tests, copied-import evidence and source preservation.
At this preparation checkpoint these controls have not run: no competing native
validation is started during the frozen model timing. Native and model results
must be recorded separately before adoption. Reused SQLite fixtures are regression
controls, not fresh independent performance validation.

한국어: 현재 비교 실행에서 표준 Path 인수를 기록하지 못해 전체 비교를 다시
실행하는 동작이 관측됐다. 정확한 표준 경로 타입의 제한된 문자열 기록을
추가하는 후보를 준비했다. 필수 테스트·실패·불완전 판정은 유지한다. 아직
이 후보의 네이티브 검사나 모델 토큰 절감은 확인하지 않았고 기본 스킬에
채택하지 않았다. 진행 중인 전체 비교가 끝난 뒤 별도 검증한다.
