# Context representation follows the actual output format

2026-09-21, parent `d151136`. Local collector correctness/output-size improvement,
not a model efficiency result.

The automatic large-file selector compared index/full-source records with default
`json.dumps` spacing even when the CLI used compact or pretty JSON. Pretty
indentation especially penalizes the nested list of definition records, whereas
numbered source is one escaped string. It could choose a larger, less informative
index and then reject the final context even when full source fit.

Reproducer:21 functions with9 assignment lines each (210 physical lines). With
the normal collector envelope and final newline, prior pretty output is4,590
characters, versus3,915 for complete source. The revised collector chooses the
complete source, retaining the hash and original line numbers. Compact still
chooses the index when it is smaller. This is675 fewer output characters on this
authored input, not a token, time or general percentage performance claim.

Size comparison now uses the requested encoder and actual selected-record nesting
depth. Shared ancestor context does not affect the difference. Explicit named/line
selectors, forced `--full`, conftest indexing and final no-partial-output limits
retain their semantics. Documentation now explicitly allows automatic
representation choice to differ by format; it no longer promises identical
records for compact/pretty automatic selection.

Four new tests cover opposing format choices, exact-fit and one-character-over
limits, multiple shapes and explicit body retention. The real100,000-character
limit is exercised with complete ancestor instructions, not just a reduced mock
budget. Author replay of the exact prior committed module fails these checks
(two failures/two budget errors); the revised module passes. This replay is not
original model evidence. Context-focused tests and the32 existing audit-context
tests pass on Python3.9/3.11. No entrypoint or featured-chart change, no claim that
the whole skill beats baseline or that all release checks were rerun.

한국어: 자동 목차 선택이 실제 출력 형식의 크기를 반영하지 않아 더 큰 결과를
고르거나 들어갈 수 있는 결과를 거부하던 문제를 수정했다. 예제에서는 전체
소스를 보존하면서675자를 줄였다. 모델 전체 성능 개선으로 과장하지 않는다.
