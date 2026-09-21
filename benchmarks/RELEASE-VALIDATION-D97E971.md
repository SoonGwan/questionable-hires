# Combined release regression — 2026-09-21

Measured source `d97e9713f800adb82f5ddba18dc57f7ec5b3f594`. This is a
compatibility checkpoint, not a skill-performance experiment. No instruction or
runtime was changed during these checks; no new model sessions were scheduled.

## Local verification

The existing macOS Python3.11.16 development environment ran
`python -B -m unittest discover -s tests -q` against the clean Git checkout:
**1,131 tests passed, zero skips/failures, 203.571s, exit0**.
Repository validation and `sync_featured_benchmark.py --check` passed.

A fresh `git archive d97e971` was extracted into a temporary directory without
`.git` or `benchmarks/local-runs`. Its repository validator and featured sync
check also passed. Full archive regression discovered1,131 tests:
**1,104 passed,27 skipped,zero failures,185.019s,exit0**. Historical-resource
checks are guarded without Git; skipped checks are not passes. The non-verbose
terminal summary records their count, not individual skip names.

The first archive test command ran before extraction finished and exited1 with
`Start directory is not importable: 'tests'`; no tests executed. After extraction
completed, explicit checks confirmed the test directory existed and Git/local-run
state did not. Only then was the actual archive suite started. This orchestration
error is not a source-test failure and is not hidden as a passing attempt.

The two full suites overlap: elapsed times are not comparative performance
measurements. Synthetic runner controls print simulated cell logs; those are not
model experiments. Terminal summaries are the retained observation for these
non-verbose runs, not a committed per-test verbose transcript.

## Hosted execution remains unavailable

[Run35598445820](https://github.com/SoonGwan/questionable-hires/actions/runs/35598445820)
at this source is terminal failure. All four jobs have empty step arrays.
Python3.11 check106328586437 explicitly says execution did not start because of
failed account payments or the spending limit. Billing, visibility and workflow
permissions were not changed. Local green checks cannot substitute for hosted
success or validate untested operating systems/interpreter versions.

## Scope

No new efficiency, automatic helper adoption, broad20–30% improvement or public
release claim follows. Frozen model results, featured graphs and both README
languages remain unchanged. The latest routing and measurement corrections are
included in the tested source, unlike older full-suite checkpoints.

한국어: 현재 커밋 작업본의 전체1,131개 검사가 통과했고, 압축본은1,104개 통과·
27개 건너뜀·실패0개였다. 압축 해제 전 시작한
첫 명령의 준비 오류도 공개하며 실제 압축본 검사와 구분한다. 원격 CI는 결제·한도
사유로 시작되지 않았다. 이번 결과는 로컬 호환성 검증이며 모델 성능 향상이나
공개 배포 완료를 뜻하지 않는다.
