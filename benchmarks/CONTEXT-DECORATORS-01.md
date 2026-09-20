# Con Artist: eliminate repeated whole-source decorator scanning

2026-09-20 · original `3a985e8` · [profile source](profile_context_decorators.py)
· [all local timings and source/output hashes](results/context-decorators-01.json).

The context collector indexed each decorator through `ast.get_source_segment`.
Inspection of the installed Python implementation shows it splits the entire
source for each call. A 200-decorator native control observed 200 whole-source
segment calls and failed the bounded-work regression before the patch.

The collector now splits physical lines once into UTF-8 bytes and shares them
through nested class indexing. AST byte offsets select the same original text.
LF, CRLF, CR, multiline decorators, Unicode and non-newline control characters
inside literals match the native extractor. Output fields, hashes, line numbers,
scope, size limits and read-only behavior are unchanged. No additional model
instructions, forced helper adoption or dependency is introduced.

Whole `collect()` calls, three alternating in-process repetitions per condition:

| Decorators | Original median | Candidate median | Output parity |
|---|---:|---:|---|
| 1 | 0.000260s | 0.000253s | identical |
| 25 | 0.014808s | 0.000783s | identical |
| 200 | 0.957693s | 0.004842s | identical |

All returned objects match, not merely excerpt counts; source bytes remain
unchanged. Timings include file/context discovery, reading, parsing, indexing and
output-size validation, but exclude interpreter startup and CLI printing. Shared
warm host, authored inputs, Python 3.9.6. The one-decorator timings are too small
to establish a meaningful gain. This is a **local algorithm improvement**, not
representative model token/time savings or evidence for the all-eight objective.

Validation: two new tests pass on Python 3.9 and 3.11; the repeated-scan test
fails before the change (200 calls versus at most one). Existing context suite:
32/32 pass. Packaging suite: 13/13 pass. Both native source-segment equality and
complete-collector equality are checked. Featured model charts remain unchanged.

한국어: 데코레이터마다 전체 파일을 다시 나누던 중복 작업을 제거했다. 200개
데코레이터 입력의 전체 수집 함수 중앙값은 약 0.958초에서 0.00484초로 줄었고
반환 객체가 완전히 같았다. 기존 문맥 검사 32개·패키징 13개와 새 회귀 검사가
통과했다. 특정 입력·로컬 도우미의 개선이며 전체 모델 작업 성능으로 주장하지 않는다.
