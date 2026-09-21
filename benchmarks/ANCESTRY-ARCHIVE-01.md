# Ancestry runner source-archive correction — 2026-09-21

Parent `faab9e2`. This fixes author-side test portability, not skill/model cost.

## Reproduced before correction

A fresh `git archive HEAD` extracted outside the checkout has neither `.git` nor
`benchmarks/local-runs`. Running `test_ancestry_scope_runner.py` with the existing
Python3.11 interpreter produced **six errors in2.251s**: each test's setup tried
to read pinned repository resources from absent Git history. The distribution
workflow runs those tests, so checkout-only green tests were insufficient.

No model benchmark is rerun or rescored. The existing six-cell result retains its
original launcher, task, resources and test-source identity at launch.

## Correction

The six scheduling/identity/limit tests now exercise the real preparation and
execution-control code using explicit synthetic resource Git objects. Their
project history is still a real independently constructed local Git repository.
Unknown repository Git requests fail; executable asset modes are checked too.
These synthetic resources never enter model runs or historical performance claims.

A separate historical-resource test uses the existing `require_history` guard.
In a checkout it checks every pinned Necromancer file's bytes/mode and complete
file inventory. In an archive or shallow checkout missing those revisions it
explicitly skips only that historical check. Schedule, changed-ref, changed-resource,
exclusive-start and account-limit controls must still run, not all skip.

The production runner, native fixture, installed skills and frozen reports are
unchanged. Only future test-source hashes differ; do not rewrite old manifests.

## After-correction validation

- Checkout Python3.11: all10 fixture/runner checks pass in7.652s, including actual
  pinned resources.
- Fresh `git archive` of`0d79b39`, verified without`.git` or`local-runs`:
  Python3.11 runs10 checks in6.333s,9pass/1explicit historical skip;
  Python3.9 runs10 in6.330s with the same9pass/1skip.
- The six previously failing scheduling checks all execute and pass in both
  archive runs; they were not converted into skipped checks.

These are targeted checks, not a rerun of the full repository suite or hosted CI.
The original failing archive remains a separate author artifact; results are not
substituted into the previously measured model records.

## Hosted boundary

Fresh inspection of [run35584332665](https://github.com/SoonGwan/questionable-hires/actions/runs/35584332665)
at`faab9e2` shows all four jobs with no executed steps. The Python3.11 annotation
reports failed account payments or a spending-limit issue. This is distinct from
the locally reproduced archive defect. Account settings were not changed, and
local validation cannot establish a hosted pass.

한국어: 소스 압축본에서 새 실행기 테스트6개가 Git 이력 부재로 실패했다.
일반 실행 제어 검사는 합성 리소스로 계속 실행하고, 실제 과거 리소스 비교만
이력이 없을 때 명시적으로 제외하도록 분리했다. 기존 모델 측정은 그대로다.
