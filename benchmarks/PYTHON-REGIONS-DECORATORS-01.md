# Preserve the opening of multiline Python decorators

2026-09-21, parent resource `7d67eff`. Correctness repair, not a model benchmark.

Necromancer's named-region helper previously took decorator starts from AST
expression locations. For valid `@(\n    decorate\n)\ndef target(): ...`, the
expression starts on line2 but the decorator starts on line1. The helper omitted
`@(`, reported start_line2 and still returned `complete: true`. Explicit backslash
continuations have the same problem. Such excerpts can mislead a history review.

The helper now lazily tokenizes when a selected function has decorators, keeping
logical-statement `@` positions rather than matrix operators or text in strings.
It locates the first decorator's opening before slicing the original source.
Universal-newline tokenization supplies physical positions; original bytes' hash,
line endings, indentation and shared12,000-character output budget are unchanged.
Tokenization is an additional pass for selected decorated functions; this is not
a speed or memory improvement claim. Undecorated selections do not need it.
No source code is executed. Existing source-size and match limits remain intact.

## Validation

- Before repair, four new regression tests fail with six assertion failures,
  including LF/CRLF/CR subcases. Tests cover exact source text and line positions,
  reparsing a complete excerpt, nested async/stacked/continued decorators,
  strings/matrix operators and truncation that counts the actual opening lines.
- After repair on Python3.11.16: all18 region tests pass,0.114s, no skips.
- Python3.9.6:18 discovered,16 pass,2 explicit syntax-version skips,0.114s.
  Skips are existing match/exception-group tests, not new decorator tests.
- Build/distribution: all13 checks pass on Python3.11.16,3.029s.
- Fresh `git archive 5956f47`, without Git or local-run artifacts: all18 region
  tests pass using Python3.11.16,0.111s, no skips.
- Catalog/document links, featured synchronization and whitespace checks pass.

Following `skill-creator`, this is a narrow code repair backed by reproductions,
not another universal model instruction. The mode guide explains the existing
decorator-preservation contract; top-level instructions and README capability
claims do not change. Frozen graphs and model outcomes are untouched. No new
whole-task gain, hosted validation or release readiness is claimed.

한국어: 여러 줄 데코레이터의 시작을 누락하고도 완전한 발췌라고 표시하던 결함을
고쳤다. 원문·줄 번호·출력 한도를 검사했으며, 모델 토큰·시간 개선 수치는 아니다.
