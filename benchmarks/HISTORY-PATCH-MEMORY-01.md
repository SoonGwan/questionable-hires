# History excerpt intermediate allocation — 2026-09-21

Parent `0154324`. `selected_patch_excerpt` retained only target-adjacent rows but
first allocated every patch line with `git_lines(body)`. Chunking that iteration
through the next LF after roughly 64K characters removes the full line list;
complete patch validation, selection, ordering, omission markers and budgets stay
unchanged. A single long row may exceed the chunk size. Full Git output and patch
strings remain in memory; this is not a subprocess/RSS cap.

Reproduce with `python3 -B benchmarks/history_patch_memory.py`. The authored input
is 40,000 added rows / 428,921 characters with targets at 1, 20,000 and 40,000.
The input is allocated before tracing; only allocations during the excerpt call
are measured. The eager control substitutes the original line-list function in
the otherwise identical parser. The outputs compare exactly.

Python 3.9.6 observed peak traced allocation: **3,131,915 → 940,928 bytes**
(about 70% lower). Ten alternating timing pairs, measured separately from allocation
tracing: median **0.024091625 → 0.024337396 seconds**, about 1.02% higher, not a
speedup claim. The first experimental per-line regex generator used 435,490 bytes
but took median 0.034505688 versus 0.023237334 seconds (about 48% slower); it was
rejected before commit. Chunking trades some of that memory reduction for avoiding
per-line regex/generator overhead. Tiny shared-host runtimes are descriptive.

49 history tests pass on Python 3.9.6 (17.527 seconds) and Python 3.11.16
(17.560 seconds). Four new tests cover exhaustive short CR/LF/Unicode strings,
64K boundaries/long lines/empty rows, eager-equivalent excerpts and malformed-tail
rejection, and substantially lower intermediate peak on a large patch. Existing
native Git controls also pass. Skill metadata/link/featured-sync checks pass.

No entrypoint change, model run, token reduction claim or graph update. This is a
bounded implementation memory improvement, not fulfillment of the all-eight
whole-task efficiency objective. New model evaluation still needs a meaningful
workload and equivalent successful work, not a favorable microbenchmark alone.

한국어: 큰 패치에서 전체 줄 목록을 추가로 만들던 할당을 줄였다. 같은 출력으로
이 함수의 추가 메모리가 약 70% 감소했지만 실행 시간 중앙값은 약 1% 증가했다.
전체 메모리·모델 토큰·개발 작업 속도가 70% 개선됐다는 뜻은 아니다. 관련 49개
검사가 두 Python 버전에서 통과했으며 기존 그래프는 변경하지 않는다.
