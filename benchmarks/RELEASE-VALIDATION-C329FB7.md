# Current-tree compatibility check — 2026-09-21

Source `c329fb7b22d132d1c103d9e0adf60b8342a923ee`. This checks the combined
changes since the [earlier full-suite checkpoint](RELEASE-VALIDATION-33498A0.md),
including audit diagnostics, routing, ZIP scheduling and compact audit output.
It is not new model-performance evidence.

| macOS environment | Python | Discovered | Passed | Skipped | Failed |
|---|---|---:|---:|---:|---:|
| Git checkout | 3.11.16 | 1,101 | 1,101 | 0 | 0 |
| Fresh committed source archive | 3.11.16 | 1,101 | 1,076 | 25 | 0 |

Both commands were `python -B -m unittest discover -s tests -q`, using the existing
development environment. Exit0 in both. Terminal summaries report197.681s and
183.652s; runs overlapped, so these are not comparative speed measurements.
No new model calls were launched: synthetic runner unit tests print simulated
cell logs, which must not be counted as model evidence.

The archive was extracted from `git archive c329fb7` into a fresh temporary
directory, with neither `.git` nor `benchmarks/local-runs`. Its repository
validator and featured-document/chart synchronization check also passed.
The non-verbose suite summary retains the skip count, not individual skip names.
Do not describe those25 skips as passing historical comparisons. Complete suite
stdout was observed through terminal calls, not retained as a repository log.
An attempted Git status/diff check in the archive correctly refused the absence
of a repository; it is not part of the passing archive validation claim.

## Hosted checks remain unavailable

Read-only inspection of [run35590793017](https://github.com/SoonGwan/questionable-hires/actions/runs/35590793017)
at this exact source found all four jobs terminal with failure and empty step
lists. Python3.11 check106304473882 reports that the job did not start because
recent payments failed or the spending limit needs increasing. This is a hosted
execution restriction, not an observed test failure. No account, billing,
visibility or workflow bypass was changed.

## Decision

Recent changes pass the complete local macOS checkout/archive regressions, not
only their focused tests. Linux/Python3.9/3.12 complete current-tree coverage is
not established by this checkpoint; the older Linux record keeps its old source.
Local green tests do not replace hosted checks, prove broad20–30% gains or grant
publication approval. Frozen model results and featured charts are unchanged.

한국어: 현재 커밋 전체 회귀 검증에서 작업본1,101개가 통과했고, Git 이력이 없는
배포 압축본은1,076개 통과·25개 건너뜀으로 종료됐다. 최신 원격 CI는 결제·한도
사유로 작업이 시작되지 않았다. 로컬 호환성 검증이며 모델 성능 향상이나 공개
배포 완료로 해석하지 않는다. 이전 Linux 결과를 현재 코드의 결과로 바꾸지 않았다.
