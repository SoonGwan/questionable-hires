# Python region traversal — 2026-09-20

The Necromancer excerpt helper now avoids visiting expression subtrees: Python
expressions cannot contain function/class statements. Statement containers remain
traversable, including conditional/loop bodies, exception handlers, match cases and
nested classes/functions. No instruction, excerpt budget or model task changed.

This is a **local helper microbenchmark**, not whole-task model performance.
The comparison uses `b8b2f3f` and the changed helper identified by source hashes in
[raw samples](python-regions-traversal-01.json). All five inputs have identical
complete result dictionaries, including hashes, text, ordering and truncation.

| Input | Before median | After median | Time change |
| --- | ---: | ---: | ---: |
| Two small functions | 33.92 µs | 32.58 µs | −3.93% |
| Large single string | 17.955 ms | 18.125 ms | +0.95% |
| Large overlapping definitions | 18.819 ms | 18.988 ms | +0.90% |
| Generated configuration, 5,000 expression rows | 103.205 ms | 60.612 ms | −41.27% |
| 1,000 functions | 17.509 ms | 13.161 ms | −24.83% |

Python-traced peak allocations are identical in every pair. Decode, parse, hash
and excerpt construction are included; CLI startup, Git and model work are not.
One warm shared host, Python 3.11.16, seven alternating timing samples per arm,
three separate allocation samples, one equality-check warmup. Synthetic workloads
and small samples do not establish a general speedup; regressions remain visible.

Validation: 14 tests pass on Python 3.11; Python 3.9 runs 12 and explicitly skips
the two unsupported syntax cases. New tests compare definition order and exact
spans with an independent unpruned AST visitor across statement containers, and
verify expression descendants are not walked. Existing text budget, duplicate,
line-ending, future-feature, invalid-input and CLI checks remain. A local
differential check additionally selected all 85 distinct per-file function names
across the 11 shipped Python helpers: all before/after dictionaries matched.
The expanded region/history regression selection passes 52 tests in 14.069 seconds;
skill metadata, repository validation and featured-chart synchronization checks pass.

Reproduce timing (requires the pinned Git history):

```sh
python3 -B benchmarks/profile_python_regions_traversal.py --output /an/unused/path.json
```

한국어: 함수 정의가 들어갈 수 없는 수식의 AST 순회를 생략했다. 조건문·반복문·
예외 처리·패턴 매칭 내부와 중첩 정의는 그대로 탐색한다. 합성 입력 5개에서
결과가 동일했고, 수식이 많은 입력은 약 41%, 함수가 많은 입력은 약 25% 빨랐다.
큰 문자열 입력 2개는 약 1% 느려졌으며 메모리 피크는 변하지 않았다. 이는
도우미 함수의 로컬 측정이지 모델 토큰·전체 작업 시간 개선의 증거가 아니다.
