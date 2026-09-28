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
