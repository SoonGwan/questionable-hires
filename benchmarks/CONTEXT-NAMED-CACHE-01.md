# Named-scope reuse — 2026-09-20

Parent `e20396f`; Con Artist collector implementation only. Named selectors
previously traversed each statement scope again for each dotted-name component.
Eight methods of one class traverse module/class scopes sixteen times. A map
within the existing parsed-file snapshot now traverses those scopes twice.
It retains duplicate names as ambiguous, never evaluates branches, and is
discarded at the end of the invocation. Entrypoint instructions are unchanged.

## Local evidence, not model efficiency

[Reproduction script](profile_context_named_cache.py), [raw samples](context-named-cache-01.json).
Fifteen alternating paired repetitions on three actual repository files; select
the first eight function definitions in source order (four when only four exist),
and each file's first function as a single-selector control. Each arm reads the
same working source. Full `collect()` results are identical in all measurements.
This includes filesystem reads, parsing and output-budget validation but excludes
CLI startup. Shared warm host and millisecond timings limit interpretation.

| Source | Selectors | Before / after median ms |
|---|---:|---:|
| collector itself | 1 | 2.054 / 2.020 |
| collector itself | 8 | 2.353 / 2.310 |
| audit context tests | 1 | 2.561 / 2.616 |
| audit context tests | 8 | 3.226 / 3.032 |
| HTTPX audit tests | 1 | 0.681 / 0.666 |
| HTTPX audit tests | 4 | 0.787 / 0.763 |

This is a small local improvement, not a large speedup: the single audit-context
selection is slower. No inference of token savings, model adoption, allocation
savings or a bundle gain. Prior screen03 observations and charts are unchanged.

Regression tests verify the two walks, exact excerpts, duplicate conditional
names, separate class scopes, missing names, and fresh source/hash after an edit.
32 audit-context checks pass on Python 3.11.16; 14 context checks pass on both
Python 3.11.16 and Python 3.9.6. No new full-suite result is inferred here.

한국어: 같은 파일의 여러 함수 이름을 찾을 때 범위 탐색을 호출 내에서만
재사용한다. 실제 저장소 파일 3개에서 출력은 모두 동일했다. 여러 정의 선택은
약 1.8–6.0% 빨랐지만 단일 선택 하나는 약 2.1% 느렸다. 작은 로컬 도구 최적화로
기록하며 모델 토큰 절감이나 전체 성능 개선으로 주장하지 않는다.
