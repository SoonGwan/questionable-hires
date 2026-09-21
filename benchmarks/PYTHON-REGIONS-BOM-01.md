# Named Python excerpts: UTF-8 signature compatibility

2026-09-22; parent `f91b652`. A valid Python file beginning with the UTF-8 BOM
compiles using native `compile(bytes, ..., dont_inherit=True)`, but the excerpt
helper decoded the marker into U+FEFF and rejected it as source syntax. The CLI
returned2 instead of a complete named excerpt. This was reproduced without
executing input code, then captured in two new regression tests (one failure,
one error before the fix).

Decode with `utf-8-sig` rather than `utf-8`, removing only an initial signature.
The original bytes still determine the2MB limit, source byte count and SHA-256.
Physical line numbers, CRLF text, decorator openings, future-feature metadata,
selection bounds and total excerpt budget remain unchanged. An interior or
second BOM is still invalid; arbitrary encoding autodetection is not added.
The reference describes the signature/excerpt distinction without changing the
skill entrypoint, discovery or adding a mandatory workflow.

Validation:

- Python3.11.16:20 region tests pass, including the two new regressions.
- System Python3.9.6:8 base region tests pass.
- Fresh source archive plus changed code/tests:20 region tests pass, without
  project history or local-run dependencies.
- Skill schema validation and diff whitespace checks pass.

This fixes rejected supported input; it is not a measured model-token/time
improvement, complete repository regression run or new featured benchmark.
The skill-creator guidance favors this narrow demonstrated repair over adding
generic instructions. No task assertions or provenance requirements were removed.

한국어: Python이 정상적으로 읽는 UTF-8 BOM 파일을 코드 발췌 도구가 거부하던
문제를 수정했다. 원본 바이트 해시·크기·줄 번호는 유지하고 첫 BOM만 처리한다.
새 회귀 테스트와 기존20개 검사를 통과했지만 모델 성능 향상 수치로 주장하지 않는다.
