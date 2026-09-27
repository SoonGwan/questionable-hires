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

## Native verification after integration06 timing

The first Git-free run retained an author-test error: it requested the
module-only `provenance_ready` field in bootstrap mode. The native result checks
preceding that assertion passed, but the control suite did not. The corrected
control checks actual copied-import lines in both modes and the additional field
only for module mode. [Original failure](results/receipt-path-observation-01-native/archive-tests.txt)
is preserved. No helper change was needed for this test repair.

All four controls now pass both in the checkout and in the six-file Git-free
archive. [Archive native output](results/receipt-path-observation-01-native/archive-tests-fixed.txt),
[checkout output](results/receipt-path-observation-01-native/checkout-tests-fixed.txt)
and [verified source hashes](results/receipt-path-observation-01-native/verified-sources.json)
are separate. The checkout log was initially given an archive-style filename;
its recorded scope here is checkout, and the separate actual archive invocation
passed afterward. There was no repository history or local model artifact in the
archive; each SQLite fixture creates its own required local commits.

The original observer stops on a Path setup assertion in each supplied SQLite
case. The candidate reaches both revisions in bootstrap and module modes, records
14 argument pairs per suite, preserves the five native tests and their genuine
failure/pass outcomes, verifies copied imports, removes its temporary copies and
preserves original file inventory. Exact native POSIX and pure POSIX/Windows
values, overlong paths, custom-subclass rejection and profile cleanup are covered.
This is not execution on native Windows or model-token improvement evidence.

한국어: 첫 검사에서 bootstrap에 없는 필드를 요구한 작성자 오류를 보존했다.
검사를 고친 뒤 저장소와 Git 없는6개 파일 묶음에서4개 검사가 통과했다. 기존
관찰기는 Path에서 중단하지만 후보는 두 리비전의5개 테스트와 실제 실패·통과를
유지하고 각14개 인수를 기록한다. 모델 토큰 절감·Windows 실행 증거는 아니다.
