# Context index allocation01 — 2026-09-28

Parent `65cd6556`. Native implementation candidate only; zero models. Searches of
the context representation-size, named-cache and region-budget reports find the
existing exact-size fallback and related allocation work, but not this shortcut.
Reuse the existing seven-pair/three-allocation profile engine rather than another
timing framework. Preserve all outcomes, including small-input regressions.

The Con Artist collector currently materializes and JSON-serializes full numbered
source for every automatic large-file index, solely to choose the smaller record.
When the serialized index is already smaller than the sum of physical source-line
character counts, that work cannot change the choice: full output additionally
contains line prefixes, separators and JSON structure, and escaping cannot shrink
the original characters. Skip full-source construction only under that strict
lower bound. For every other case retain the existing exact, format-aware size
comparison. Explicit selectors, full reads, limits, input hashes and outputs stay
unchanged. This does not omit requested context or relax an output guard.

Before adoption, require exact old/new collect-result and serialized-output
equality for compact/pretty small input, sparse large source, dense fallback,
representation crossover and an actual repository-source control. Every timed and
allocation invocation must match its warmup result. Use the existing alternating
seven timing pairs and three separate tracemalloc pairs; no favorable rerun.
Measure full collect() including reads, parsing and output validation, excluding
CLI startup. Traced allocation is not RSS or total memory.

Run existing representation/budget, named/line/group selection, Unicode/BOM and
decorator controls in checkout and a fresh Git-free source copy with supported
Python3.9/3.11. Preserve exact output-limit errors and complete ancestor context.
Do not add model trials unless the change reaches an observed costly model path;
native milliseconds/allocation do not establish whole-task tokens or latency.
No featured benchmark or historical costs are relabeled.

한국어: 짧은 정의 목록을 선택할 것이 확실해도 전체 소스 출력을 다시 만들던
작업을 줄인다. 안전한 길이 하한으로 확정할 수 없으면 기존 정확한 크기 비교를
그대로 수행한다. 반환 내용·출력 한도·해시는 보존하고 모든 원본 측정을 남긴다.
로컬 시간·메모리 최적화이며 모델 토큰 절감이나 전체8개 성과로 계산하지 않는다.
