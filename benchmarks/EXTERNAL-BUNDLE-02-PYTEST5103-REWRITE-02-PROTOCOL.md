# pytest5103 warning-policy distinction02 — 2026-09-28

Parent `10acee70`; preserve all six original
[rewrite01 diagnostics](results/external-bundle-02-pytest5103-rewrite01/authored-results/observations.json).
Direct and native scalar/generator/list examples all produce the expanded expected
assertion. Native generator/list each additionally emit SyntaxWarning about an
identity comparison with a literal. Native `assertmode` is rewrite in all three.
The original protocol's third branch applies: simple native loading works; the
original issue context is still missing. Do not call this an issue fix.

The first diagnostic's `rewritten` flag checks only function `co_names` and is
false for both transformed all(...) functions despite expanded assertion output.
It is an incomplete marker, not evidence of absent transformation. Preserve the
field unchanged and use actual output. Static gold transformation places imports
inside the function; that can use local variable names instead of global names.

The selected project's original tox.ini configures warnings as errors. Its pytest
import loader catches SyntaxError from compiled transformed AST and falls back to
ordinary loading. This gives a specific hypothesis: turning the observed
SyntaxWarning into an error prevents transformed code from being loaded, leaving
a plain assertion message. Do not presume a Python-version/cache explanation.

Freeze six distinct cells with the same three authored sources and same original
gold source as rewrite01: direct AST transformation adds only
`warnings.simplefilter('error', SyntaxWarning)`; native pytest adds only
`-W error::SyntaxWarning`. This isolates the observed category rather than modifying
the project, its original warnings policy or issue tests. Expected discriminating
outcome: scalar remains expanded; the two all(...) direct compilations raise an
actual compiler diagnostic and native loading falls back to a plain assertion.
If not, preserve the result and do not promote the hypothesis.

Reuse the pinned image, offline wheels, installed import, source guards, same
resource/time bounds, container restrictions and terminal cleanup from
[rewrite01 protocol](EXTERNAL-BUNDLE-02-PYTEST5103-REWRITE-01-PROTOCOL.md).
No issue cells, original labels, parser, gold patch, dependency or registry change.
Do not turn this diagnostic into accepting a relaxed warnings policy or rerunning
the original pair. Retain all errors and six outcomes; no unchanged retry.
Private issue data stays outside repository/model contexts. Export only authored
diagnostics and hashes. Zero models, no skill/performance/public-release change.

한국어: 첫6개 진단에서는 직접 변환·실제 로딩 모두 확장 메시지가 나왔다.
두 표현식에서만 나온 SyntaxWarning과 원본 프로젝트의 경고 오류 정책을 대조한다.
해당 경고 처리만 바꾼 새6개 대조군을 고정하며, 원본 경고 정책이나 채점 조건을
완화하지 않는다. 실제 출력과 불완전한 바이트코드 표시를 구분한다.
