# Context index allocation01 — 2026-09-28

The collector now avoids constructing full numbered source when a strict lower
bound already proves the automatic definition index is smaller. Returned objects,
serialized output, source hashes and limits stay identical. This removes native
allocation work; it does **not** establish fewer model tokens or whole-task latency.

Previous `65cd6556`, [protocol](CONTEXT-INDEX-ALLOCATION-01-PROTOCOL.md) `f3a9f4f8`,
implementation and profiler `f416c8d9`. The index's serialized length is compared
with the sum of physical source-line character lengths. Full numbered JSON source
cannot be shorter than those contents. If that strict inequality does not settle
the choice, the original exact compact/pretty comparison remains. Explicit body
selection and full-file reads are unaffected; no requested context is dropped.

[Profiler adapter](profile_context_index_allocation.py) reuses the existing
[allocation engine](profile_python_regions_budget.py). All
[original measurements](context-index-allocation-01.json) are retained: one equality
warmup per arm/case, seven alternating timing pairs, three separate tracemalloc
pairs. Every invocation returns identical objects and exact serialization. Four
synthetic shapes and one copied repository-source control run in both formats.

| Workload / format | Before → after median ms | Time change | Traced peak before → after bytes |
| --- | ---: | ---: | ---: |
| Small / compact |0.1734 →0.1708|−1.49%|267,649 →267,649|
| Small / pretty |0.1922 →0.1864|−3.01%|267,649 →267,649|
| Sparse large / compact |3.6355 →2.8511|−21.58%|1,073,723 →928,675|
| Sparse large / pretty |3.6430 →2.9641|−18.64%|1,077,833 →928,675|
| Dense fallback / compact |1.5256 →1.5271|+0.10%|982,778 →982,778|
| Dense fallback / pretty |2.2813 →2.2597|−0.95%|982,778 →982,778|
| Format crossover / compact |0.7080 →0.7131|+0.72%|505,494 →505,494|
| Format crossover / pretty |0.7774 →0.8082|+3.97%|506,474 →506,474|
| Repository tests / compact |2.9041 →2.8228|−2.80%|2,214,104 →2,214,104|
| Repository tests / pretty |3.2920 →3.3184|+0.80%|2,214,104 →2,214,104|

Sparse-large traced peaks decrease13.51%/13.84%. Other traced peaks are unchanged;
four timing rows regress. The workload emphasizes long source with a short index,
not a representative project distribution. Shared warm host, one interpreter and
submillisecond differences limit timing inference. Git announced background
auto-packing immediately before profiling; overlap with individual samples was
not monitored, so host housekeeping interference cannot be excluded. No favorable
rerun is substituted. Tracemalloc records Python allocations, not RSS or a memory
bound. Timing includes collect() reads/parsing/budget checks and chosen-result
serialization, excluding CLI startup.

## Correctness and decision

The existing39 context checks pass in checkout. An added regression verifies the
shortcut's exact output boundary, complete ancestor instructions and original
identity with BOM, Unicode, escaped characters, tabs and LF/CRLF/CR input; all five
representation tests pass. These are preserved-output checks, not a previously
incorrect result changed to correct. Both native formats still reject one character
below the required output budget without partial context.

Fresh Git-free copies run72 context/audit tests successfully on Python3.11 and3.9.
[Original logs and dependency record](results/context-index-allocation01/) retain
the first copy's one FileNotFoundError: the author initially omitted the reference
used by the documented-command test. Adding that explicit unchanged Markdown
dependency corrects preparation; the original72-test error run remains, and is not
counted as a pass. No source change or skipped test repairs it.

Adopt this output-preserving native optimization. Do not rerun integration07 solely
because the package changed: its original Con Artist workflow did not use this
collector. This measurement supplies no model-level gain, generalized speed claim
or change to the all-eight unmet decision. Historical charts and published whole-task
costs retain their original measured resources. Delivery is verified separately.

The installed previous resource matched the pinned baseline before replacement;
its backup remains. All eight local installations now match checkout bytes/modes,
and five representation/budget tests run against the actual installed collector.
The rebuilt download's52 resources match source bytes/modes; standalone archive4
and landing31 tests pass. These delivery checks are not new model measurements.

한국어: 짧은 정의 목록을 선택할 것이 확실한 경우 버릴 전체 소스 문자열을
만들지 않는다. 반환 객체·문자열·해시·한도는 모두 동일하다. 큰 합성 사례는
시간18.64–21.58%, Python 추적 메모리13.51–13.84% 감소했지만 시간 증가4행도
그대로 보존한다. 전체 프로세스 메모리나 모델 토큰 절감은 아니다. 새 경계 검사와
Git 없는 사본72개 검사가3.9/3.11에서 통과했으며 최초 누락 파일 오류도 남긴다.
원본 모델 경로가 이 도구를 쓰지 않았으므로 단순히 새 패키지라는 이유로 전체
실험을 반복하지 않는다. 전체8개 품질·토큰·시간 목표는 미달이다.
