# Con Artist line-selector traversal — 2026-09-20

Local function microbenchmark only, **not GPT token/time evidence**. Previous
collector `ff474e5` traversed all AST nodes separately for every line selector.
The change builds definition spans once per invocation-local parsed source and
reuses them. Named selectors do not build this index. Definitions, decorators,
nested scopes, ambiguous locations, excerpts, hashes and limitations are retained.

[Reproducer](profile_context_lines.py), [all samples/source hashes](context-lines-01.json).
Two synthetic source sizes and one/eight line selectors, seven repetitions each,
alternating old/new order after one equality-check warmup per arm/workload.
Every full returned result matches exactly, including hashes and source excerpts.

| Definitions | Selected lines | Old median ms | New median ms | Change |
| ---: | ---: | ---: | ---: | ---: |
| 50 | 1 | 1.979 | 1.921 | −2.93% |
| 50 | 8 | 8.873 | 2.095 | −76.38% |
| 500 | 1 | 18.511 | 18.783 | +1.47% |
| 500 | 8 | 84.294 | 18.879 | −77.60% |

The measurements cover `collect`, including read, parse and output-limit JSON
serialization, not process startup or model execution. Warm filesystem/shared
host, one interpreter, synthetic source and few samples limit interpretation.
The small one-selector variation is retained; do not claim every call improves.
The absolute saving is milliseconds, not minutes or model-token reductions.

Four new behavioral tests compare every source line against the prior resolver,
assert a single traversal for eight selectors, preserve equal-span ambiguity,
and confirm source edits invalidate all context on the next call. Existing 32
collector tests and four decorator/read-replacement tests also pass (40 total).
No real project is imported/executed for source collection. No model benchmark
chart, release-performance claim or all-eight outcome is changed.

한국어: 같은 파일의 여러 줄을 선택할 때 AST 탐색을 한 번만 수행하도록 했다.
합성 파일의 8개 위치 선택은 로컬 함수 중앙값 기준 76~78% 단축됐고 전체 출력은
동일했다. 1개 위치 선택은 거의 차이가 없고 큰 파일에서는 1.47% 증가도 있었다.
이는 밀리초 단위의 도구 최적화이며 모델 전체 속도·토큰 개선율이 아니다.
