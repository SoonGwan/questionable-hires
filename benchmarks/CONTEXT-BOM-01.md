# Context UTF-8 signature01 — 2026-09-28

Parent `18e8ed31`. Con Artist's context reader accepted UTF-8 text but decoded an
initial BOM into U+FEFF. Named/line/group selection and ancestor conftest indexing
then rejected valid Python source. Native `compile(bytes, ..., dont_inherit=True)`
accepts the same controlled input without executing it. The real CLI exited2
instead of returning the selected definition. Full text also displayed the marker
as a character. This reuses the previously verified
[Necromancer signature repair](PYTHON-REGIONS-BOM-01.md), not an independent discovery.

Decode the existing bounded byte snapshot with `utf-8-sig`. Only the initial
signature is omitted from parsed/displayed UTF-8 context, including instructions
and configuration. Original raw bytes still determine file/total input limits and
SHA256; sources/modes are unchanged. Interior literal markers survive. A duplicate
or noninitial marker outside a string still fails Python parsing; invalid UTF-8
remains unsupported. No arbitrary coding-cookie detection or input execution.

Five new methods initially produce3 assertion failures and4 syntax errors. After
the one-line behavior change,39 focused context methods pass. Explicit Git-free
copies run71 context/ancestor checks on both Python3.11.6 and3.9.6, no skips.
Controls cover named/line/group selectors, the first multiline decorator under
LF/CRLF/CR, Korean decorator expression columns in ancestor indexes, instruction
text, full source, raw byte/hash limits, unchanged0600 input modes and real CLI
success/incomplete output. Input containing a top-level raise is never executed.

[Native logs and identities](results/context-bom01/) retain the old/fixed source
and regression hashes, original-log hashes and path-redacted reading copies.
The first CLI success assertion failed before its later invalid-input controls
could run on old source; those execute after the fix. Do not count unexecuted
before assertions as verified old behavior. Git-free repetitions are portability
checks, not independent task/model observations.

No entrypoint, model setting, benchmark case, performance metric or featured chart
changes. The existing eight-role screen does not exercise this repaired input
path; it is not grounds to rerun that screen unchanged. Installation/package/public
verification follows separately. This native correction does not establish whole-
task token/time reduction or the owner's complete eight-role objective.

한국어: 정상 UTF-8 BOM Python 파일의 이름·줄·정의 모음·상위 conftest 선택이
실패하던 경로를 수정했다. 처음의 마커만 표시·파싱에서 제외하고 원본 해시와
바이트 한도, 줄 번호와 내부 문자, 파일 모드는 보존한다. 새5개는 수정 전
실패3건·구문 오류4건을 재현했고, 수정 후39개와 Git 없는 양 Python71개 검사가
통과했다. 기존 방식 재사용이며 모델 절감·전체8개 성공으로 확대하지 않는다.

## Installation and package checks

Source6208466b: verify every existing Con Artist installation file against18e8ed31
bytes/modes, move that exact directory to an owned backup outside discovery, then
install the correction. The same five new methods pass against the installed
module/CLI, and all eight installed skills match checkout bytes/modes. The archive
contains all52 exact skill resources. Four standalone archive checks and31
landing/origin checks pass; the initial wrongly named package discovery runs0
tests and is retained, not counted.

## Hosted verification — 2026-09-28

Release `bca0130f` includes source `6208466b`. All eight checked public HTTPS
routes match the deployed release bytes: health identity, Korean/English pages,
three page assets and both download files. The public archive contains all52
source resources with matching names, bytes and modes. Its108,928 bytes have
SHA256 `9507e3a0b867cfbee7e3daad7497832735cbe2028786b24d6f76a4552374852d`.
[Route and archive evidence](results/context-bom01/hosted.json) records each
response identity. This verifies release delivery; no new browser interaction
or model performance experiment was run.

한국어: 공개 배포 `bca0130f`의8개 HTTPS 경로가 배포 파일과 일치하며,
다운로드의52개 자원이 수정 소스와 이름·내용·모드까지 일치한다.
배포 전달 확인이며 새 브라우저 검사나 모델 절감 실험은 아니다.
