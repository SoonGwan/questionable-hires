# Necromancer bounded excerpt allocation — 2026-09-20

Previous source `d087a96` copied every matched function's complete text before
applying its shared 12,000-character output limit. Overlapping nested definitions
could duplicate large bodies many times. The new implementation retains physical
line offsets and slices only the remaining allowance per region. All definitions
are still visited, including those after exhaustion; missing/matching metadata,
20-match rejection, decorator ranges, original line endings, hashes and explicit
truncation remain unchanged. No parsing, matching or verification is skipped.

[Reproducer](profile_python_regions_budget.py),
[all samples and source/output identities](python-regions-budget-01.json).

| Synthetic workload | Old / new median ms | Time change | Old / new peak traced bytes |
| --- | ---: | ---: | ---: |
| Small, two complete excerpts | 0.04050 / 0.04071 | +0.51% | 13,357 / 13,437 |
| One 1.8 MB function | 20.556 / 19.864 | −3.37% | 7,222,897 / 7,212,405 |
| Ten overlapping functions, 1.8 MB body | 22.100 / 20.428 | −7.57% | 23,454,926 / 7,228,466 |

Overlapping workload peak traced allocation decreases **69.18%**. This is a
synthetic stress case, not typical-repository memory savings. Small-input variation
and allocation increase are retained. Returned dictionaries match exactly on all
workloads and every measured invocation, including full/empty truncated text and
all metadata; input and output hashes are recorded.

Seven alternating-order timings after one equality warmup per arm/workload.
Three separately instrumented `tracemalloc` runs after garbage collection measure
Python-traced peak allocation, **not RSS, total process memory or a memory bound**.
Function timing includes decoding, AST parsing, selection and hashing, not CLI/Git
startup. Shared warm host, one interpreter and synthetic inputs limit inference.
No model sessions, tokens, latency or general speedup are measured here.

Four added regression tests cover overlapping Unicode excerpts after exhaustion,
exact allowance with LF/CRLF/CR and final-line variants, decorated async definitions,
and rejecting excess matches even after the text budget is exhausted. Existing
six region tests also pass on Python 3.9 and 3.11. Related history discovery passes
44 tests in 16.906 seconds; skill/repository and featured-language checks pass.
This is an implementation optimization, not proof
that all eight skills now meet the end-to-end performance objective. No historical
model results, charts or release claims change.

한국어: 최대 출력 길이를 적용하기 전에 큰 함수 본문을 반복 복사하던 작업을
제거했다. 중첩 함수 10개·1.8 MB 본문이라는 합성 사례에서 Python 추적 메모리
피크가 69.18%, 함수 실행 시간이 7.57% 줄었다. 모든 반환 결과는 동일했다.
작은 입력은 시간·메모리가 소폭 증가한 수치도 그대로 남긴다. 프로세스 전체
메모리나 모델 토큰·속도 측정이 아니며 AST 파싱의 메모리 상한을 보장하지 않는다.
