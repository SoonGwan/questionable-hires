# Con Artist recipe keys01 — 2026-09-28

Parent `6f8cc35f`; exact before/after helper and regression-source hashes are in
[native-check.json](results/audit-recipe-keys-01/native-check.json).
Native input-correctness change, not a model experiment or efficiency result.

The audit CLI previously accepted duplicate JSON object keys, keeping the last
value. An earlier mutation's `new` value could silently disappear, and the audit
would execute the replacement value instead. The same ambiguity applied to nested
mutation entries and probe-file mappings. Receipt already rejects such recipes;
Con Artist's independent, standalone parser did not.

The CLI now rejects duplicate keys while decoding file or stdin input, before
selecting single/batch mode or reading/executing the project. JSON escape aliases
of the same decoded key are duplicates. Reusing the same key in **different**
objects remains valid. Direct Python dictionaries retain their existing API;
duplicate lexical JSON keys cannot be recovered from an already-created dict.

Errors exit2 with empty stdout, identify the escaped key, cap its displayed name
at240characters plus an ellipsis, and omit values. Valid schemas, native commands,
baseline reuse, outputs and project-preservation behavior are unchanged. No
dependency or additional entry instruction is added. The core interface and both
README capability rows describe the new input contract.

## Failing before, passing after

[Six regression methods](../tests/test_audit_recipe_keys.py) invoke the real CLI
with actual project source and native unittest support. They cover top-level
mutation replacement, escaped aliases from a file, nested batch mutation keys,
nested probe-file keys, diagnostic escaping/bounds, and a valid two-mutation batch
whose distinct objects legitimately share field names.

The initial checkout run has5failures/1pass. In a fresh Git-free archive of the
parent with only the new tests added, [before.txt](results/audit-recipe-keys-01/before.txt)
reproduces those5failures. Four otherwise valid ambiguous recipes return0 and
execute native audits instead of being rejected. The diagnostic control receives
the old unknown-field error rather than a duplicate-key error. The valid batch
passes before and after, with mutant exits0/1; this is actual native execution,
not a mocked parser.

After overlaying the changed helper, [after.txt](results/audit-recipe-keys-01/after.txt)
records **127 distinct methods passing**, no skips. This includes the six new
methods, existing mutation helper behavior, exact probe edits, module invocation,
pytest batching, project guards, output forms and selection-cache controls. Tests
check source bytes/modes and scratch removal. The diagnostic method additionally
reaches its long-key case after its first assertion is repaired by the parser fix.

These are native source-archive checks, not evidence of lower model tokens or
faster whole-task completion. No new model calls, historical metric adjustments
or featured changes occur. Hostage and Mother instruction candidates remain
declined; this fix does not reverse their measured decisions.

한국어: Con Artist가 JSON 중복 키의 마지막 값을 조용히 실행하던 문제를 고쳤다.
최상위·중첩·이스케이프 동일 키를 파일/stdin 입력에서 실행 전에 거부하고,
서로 다른 객체의 정상적인 같은 필드명은 허용한다. 실제 CLI 회귀5개가 수정
전 실패·수정 후 통과했으며 Git 없는 아카이브에서 기존 검사를 포함한127개가
모두 통과했다. 오류는 키만 표시하고 값을 출력하지 않는다. 모델 토큰·시간
절감 실험은 아니며 이전 불리한 측정이나 대표 수치는 바꾸지 않는다.

## Local delivery

Source `829a2b02` is installed on the owner's Mac with the previous Con Artist
folder backed up outside skill discovery. [Installed inventories](results/audit-recipe-keys-01/installed.json)
match the source for all8 hires; [six actual installed-CLI checks](results/audit-recipe-keys-01/installed-checks.txt)
pass. The initial precheck stopped before mutation because extracted Git archive
modes were0664 while Git/live modes were0644. Exact parent bytes and `git ls-tree`
modes resolved this author check mismatch; no owner changes were overwritten.

The regenerated downloadable archive is104,809bytes, SHA-256
`b4bc524b78aec2c780112c8df4c12dd7695490132e79b7fcacf6d1d0e3635812`.
All19 landing checks pass, including installation of exact packaged resources,
static KO/EN metadata and preservation of every historical benchmark cell.
Public delivery is a separate check; this section establishes local installation
and generated download bytes only.

한국어: `829a2b02`를 Mac 실제 설치본에 반영했고 기존 폴더를 백업했다. 전체8개
리소스가 소스와 일치하고 실제 설치 CLI6개·랜딩19개 검사가 통과했다. 초기 권한
대조 오류는 변경 전에 중단됐으며 Git의 실제 권한과 내용으로 재확인했다.

## Public delivery

Hosted release `1781c1ce` passes origin and public HTTPS identity checks. The
[public retrieval](results/audit-recipe-keys-01/public-delivery.json) matches the
complete archive and checksum file byte-for-byte against the generated download;
the packaged audit helper matches source `829a2b02`. Both static language pages
serve their expected language and download link. Existing design and historical
model evidence are unchanged; this delivery does not imply new browser QA or
model-efficiency measurements.

한국어: 공개 배포 `1781c1ce`의 HTTPS 상태와 한영 페이지를 확인했다. 공개 주소에서
다시 받은 다운로드·체크섬·내부 감사 코드가 수정 소스와 일치한다. 실제 설치본과
공개 다운로드 반영까지 완료했으며 모델 토큰 절감이나 새 화면 검증 주장은 아니다.
