# Whole-checkout validation — 2026-09-21

Code/test checkpoint `3fa1758`; analysis-only documentation/JSON additions were
in progress during this check. No runtime or test edits were made during it.

```sh
benchmarks/local-runs/receipt-provenance-venv/bin/python -B -m unittest discover -s tests
```

Python3.11.16: **1,052 tests in179.745s, OK; no failures or skips reported**.
This updates the earlier whole-checkout `c258570` result of1,035 tests.
The measured command exited0; there is no live test process remaining.

The newer set includes packaged native recipe/source-root/existing-witness
controls, edit/dateutil/slugify fixture and runner checks, in addition to the
existing eight-role helper, packaging, installer and evidence-tool checks.
Some runner tests print simulated model-cell starts/completions and expected
argument errors. Those are test doubles/negative controls, not additional model
benchmarks or performance observations. No model sessions were launched as part
of this checkpoint and no timed model session ran concurrently.

Repository validation, featured bilingual synchronization check and whitespace
check pass. Worktree scope after execution contains only this checkpoint and
the accompanying slugify input-cost analysis/status changes; no user changes
were removed. No source-archive full-suite or hosted-CI result is asserted here.

Passing tests establish local regression evidence only. They do not prove every
real project works, current hosted billing/check status, independent model
generalization, broad token/time gains or readiness to advertise20–30% gains.
The [current candidate index](CURRENT-CANDIDATE-STATUS.md) retains those gaps and
the mixed/adverse model comparisons. Featured images/numbers remain frozen.

한국어: 현재 코드 기준 전체 회귀 검사1,052개가179.745초에 통과했다. 스킵이나
실패는 없었다. 실행기의 모의 세션 출력은 새 성능 측정이 아니며, 로컬 검사
통과를 전체 성능 향상·호스팅 검사 성공·공개 배포 승인으로 확대하지 않는다.
