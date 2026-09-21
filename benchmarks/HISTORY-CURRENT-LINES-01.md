# Current-source line allocation — 2026-09-21

Parent `994d056`. Necromancer's history collector previously split every current
source row into a list even when selecting only 1–100 lines. The patch instead
counts LF rows in chunks, allocating lists for selected chunks and the final
chunk. Full UTF-8 decoding still precedes selection; missing rows still fail
before Git. No skill entrypoint, task criteria or model result changed.

## Local measurement, not model performance

[Retained nine samples per variant and source digest](results/history-current-lines-01/measurement.json)
come from `benchmark_history_current_lines.py`. Each pair alternates order;
memory is measured separately using tracemalloc. Inputs are already-decoded
strings, so this excludes file reads, decoding, Git, model tokens and full-task
latency. Eager reference is the old `git_lines` plus indexed selection. Results
are identical in all four authored inputs; no timing superiority assertion is
used as a test gate.

| Input / selection | Eager median | Selected median | Eager peak bytes | Selected peak bytes |
| --- | ---: | ---: | ---: | ---: |
| 1.9M characters, 190K short rows, first/middle/last | 3.511ms | 1.137ms | 12,647,568 | 499,151 |
| Same source, first row only | 2.979ms | 0.138ms | 12,647,440 | 498,933 |
| 1.9M characters, one long row | 0.590ms | 0.637ms | 432 | 220 |
| 300 characters, first/middle/last | 0.0010ms | 0.0013ms | 2,492 | 2,280 |

The many-short-row intermediate peak falls approximately96%; this is **not96%
less total tool memory**. The long-row and small cases are slower. Initial local
prototype counted the final chunk and then split it, doubling the long-row
median from0.594ms to1.230ms; splitting that final chunk once reduced this
regression. Those initial terminal observations were not a model run and no
complete raw prototype artifact was retained. The final measurement above
retains every sample, including adverse cases.

## Verification and scope

New controls compare LF semantics against the old implementation across short
combinations (CR, LF, Unicode separators and Korean text), chunk boundaries,
long rows, distant selections, missing rows and100selected rows. Unselected
invalid UTF-8 must still fail before Git. A traced-allocation control requires
less than half the old intermediate peak on the many-row fixture; it makes no
timing promise. Existing real-Git attribution, range and patch tests also run.

Python3.11.16: all54 `test_history*.py` tests passed in17.969s. Python3.9.6:
the four new selection tests passed in0.108s. Skill validation, repository link
validation, featured synchronization and whitespace checks passed. This is a
targeted check of the new revision, not a rerun of the previous1,079-test suite.

Keep this bounded allocation improvement. Existing source-size limits, source
whitespace, selected output, history scope and concurrency limitations remain.
It does not explain previous unused-helper model costs or establish a broad
20–30% performance gain. Featured charts remain tied to their frozen data.

한국어: 현재 파일의 일부 줄을 선택하면서 전체 줄 목록을 복사하던 할당을 줄였다.
짧은 줄이 많은 입력에서는 해당 처리 단계의 시간·메모리가 감소했지만, 긴 한 줄과
작은 입력은 소폭 느려졌다. 전체 모델 성능이나 토큰 절감 수치가 아니며 모든
비교 결과와 제한을 공개한다. 대표 그래프는 바꾸지 않는다.
