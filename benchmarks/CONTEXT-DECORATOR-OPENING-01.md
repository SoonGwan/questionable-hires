# Context decorator opening01 — 2026-09-28

Parent `e81cc324`. Con Artist's context collector used AST decorator expression
positions as definition starts. Valid `@(\n    decorate\n)` and backslash-continued
decorators start before their expressions. Named excerpts omitted that opening;
selecting the opening line could incorrectly report that no definition encloses
it. Group/index ranges likewise pointed after the actual start.

This is the same known mechanism repaired in
[Necromancer's region selector](PYTHON-REGIONS-DECORATORS-01.md), found in the
separate context implementation. It is not a new independent discovery or a repeat
model experiment. Prior [decorator indexing optimization](CONTEXT-DECORATORS-01.md)
concerned repeated expression extraction; its historical measurements stay unchanged.

The collector now lazily tokenizes the captured source to locate logical-statement
opening `@` tokens, excluding matrix operators and apparent decorators inside
strings. The snapshot cache shares that scan across selected definitions, nested
indexing and line lookup. Named excerpts, group ranges, index ranges and actual
line selection use the physical opening. Index `decorators` fields still contain
the same expression segments. Undecorated selections need no tokenization.
No project source executes; no third-party dependency or file write is added.

[Five regression methods](../tests/test_context_decorator_opening.py) cover exact
numbered output across LF/CRLF/CR, Unicode, source hashes/modes, actual opening-line
selection, duplicate definition groups, index expression preservation, stacked and
nested async decorators, strings/matrix operators, backslash continuations and the
real CLI against a module that raises if executed.
[Before](results/context-decorator-opening01/before.txt):6 assertion failures plus
1 expected-to-work line-selection ValueError across5 methods. The line-selection
error is the actual helper defect, not a failing assertion-support setup.
[After](results/context-decorator-opening01/after.txt):all34 `test_context*` methods
pass. Assertions themselves are unchanged; an unused test import was removed.

The first archive command used the broader `*context*` filename pattern and
inadvertently selected unrelated benchmark-runner/candidate inspection tests.
[That attempt](results/context-decorator-opening01/python311.txt) retains73 methods
with3 missing benchmark-dependency errors. It is not a complete source archive
validation. A separate explicit copy of `test_context*` plus `test_audit_context`
and the full Con Artist resources has no Git/history or benchmark dependencies:
**66 methods pass on [Python3.11](results/context-decorator-opening01/focused311.txt)
and [Python3.9.6](results/context-decorator-opening01/focused39.txt), no skips**.
This covers prior context bounds, races, cache, group and representation behavior.

Tokenization adds work for selected decorated definitions; no native speedup or
model-token/time saving is claimed. The declared output bound still applies to
the complete numbered result. Top-level skill instructions, frozen featured and
integration07 costs remain unchanged. Existing guide-shortening/routing candidates
remain declined; this correctness fix does not justify repeating them.

한국어: Con Artist가 여러 줄 데코레이터의 실제 시작을 빼거나 시작 줄을 정의
밖으로 잘못 처리하던 경로를 고쳤다. Necromancer에서 이미 확인한 원인과 같으며
독립 성능 근거가 아니다. 수정 전5개 검사에서6개 실패·1개 실제 선택 오류가
나왔고, 이후 관련34개와 Git 없는 명시적 사본66개가 Python3.9/3.11에서 통과했다.
잘못 넓게 선택한 최초 사본의 의존성 오류3개도 보존한다. 모델 호출0회이며
토큰·시간이나 전체8개 목표 달성으로 주장하지 않는다.

## Installation and downloadable delivery

Source **`a1056d22`** is installed after verifying the previous Con Artist directory
against parent bytes/modes and moving its backup outside discovery.
[All8 installations match](results/context-decorator-opening01/installation.json);
[the same5 actual installed-source tests](results/context-decorator-opening01/installed.txt),
[package4](results/context-decorator-opening01/package.txt) and
[landing/server27](results/context-decorator-opening01/landing.txt) pass.
The151-file build check passes; only the download archive/checksum change in
landing output. [All52 packaged resources](results/context-decorator-opening01/download.json)
match source bytes/modes. Archive108,792bytes, SHA256
`59d6385f9e1a9f77ff67382ef2bfd1e84e0b39a3751c543422d1e555f050a215`.
An initial author inventory mistakenly included root skills/README.md, which the
standalone package intentionally excludes; that KeyError is disclosed in the
inventory. The corrected selection follows the existing eight skill-directory
contract and does not drop a required runtime file.

한국어: 소스a1056d22를 기존 설치본 일치 확인·외부 백업 후 설치했다. 설치 자원8개와
다운로드52개 리소스가 일치하고 실제 설치본5개·패키지4개·랜딩27개 검사가 통과했다.
최초 목록 검사의 제외 대상 카탈로그 선택 오류도 기록하며 모델 절감과 구분한다.

## Public verification

Release **`f11d059f49fde20a274de5490b86d1415ac6ac69`** is live on
[한국어](https://hires.no-money-do-you-have-money.com/ko/) and
[English](https://hires.no-money-do-you-have-money.com/en/).
[Eight HTTPS observations](results/context-decorator-opening01/public.json) match
health revision, both locale pages, runtime/style/copy assets and exact archive/
checksum bytes. All52 public packaged resources match source bytes/modes.
Canonical/indexable metadata and frozen integration07 counts are preserved.
No fresh browser interaction, model-cost result or GitHub push is claimed.

한국어: 공개 배포f11d059f의 HTTPS8개 경로와 다운로드52개 리소스 일치를 확인했다.
설치본과 공개 다운로드에 수정이 반영됐으며 대표 수치·전체8개 미달 판단은 유지한다.
