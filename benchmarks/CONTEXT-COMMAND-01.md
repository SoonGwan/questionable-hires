# Context collector command examples01 — 2026-09-28

Parent `c2fe1885`. The two executable shell examples in Con Artist's context guide
used the absent `python` alias on this Mac. Both actual code blocks, with only
installed-script/project path placeholders substituted, exit127 before collection.
[Before observations](results/context-command01/before.json) retain those shell
errors. The installation docs and other standalone collector commands already use
`python3`; project-interpreter placeholders and descriptions of module invocation
are different interfaces and are preserved.

The two examples now use `python3`, with a short note to substitute the project's
Python3.9+ executable when appropriate. [After observations](results/context-command01/after.json)
show both commands exit0: full test source plus the selected Store.save body, then
the same-name definition group. Expected representations and actual source content
are checked. The fixture's service raises immediately if executed; collection does
not execute it. Original bytes/modes remain unchanged; scratch is removed.
[Source/environment identity](results/context-command01/identity.json) records the
actual interpreter version, guide and scratch checker hashes.

This is a narrow command-example correction, not a revived interpreter-selection
paragraph. [The declined Mother experiment](MOTHER-INTERPRETER-01-REVIEW.md) remains
adverse. Con Artist's entry, metadata, helpers and required runner semantics are
unchanged. No model is invoked; no whole-task token/time savings follow from these
two local command observations. README capabilities and featured measurements
remain applicable and unchanged. Installation/public delivery are separate checks.

한국어: 이 Mac에 없는python별칭을 사용하던 맥락 수집 예제2개에서 실제127실패를
재현했다. python3로 고친 동일 예제는 모두0으로 완료되며 원본 보존과 실제 소스
내용·출력 구조를 확인했다. 필요하면 프로젝트의 Python3.9+ 실행 파일을 쓰도록
명시했다. 스킬 본문·런타임·필수 실행 계약은 바꾸지 않았고 모델 절감 실험도 아니다.
