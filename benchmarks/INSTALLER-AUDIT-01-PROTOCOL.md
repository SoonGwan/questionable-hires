# Installer audit transfer 01 — 2026-09-15 KST

Preregistered before model execution. Two authored tasks on actual pinned project
code, not organic maintainer issues or an independent holdout. Both share one
installer and four tests, so they are not independent coverage of two repositories.

Use [the native preflight](INSTALLER-AUDIT-PREFLIGHT-01.md) and its exact 11 input
files from `07166bfcca6432f3954b6e1fb88e555acfe11d2a`, with only the disclosed
project-local test setup adaptation. The generator adds project instructions but
does not supply author faults, expected verdicts or preflight observations to the
model. Bundled `skills/` files are payload data, explicitly not active instructions.
Freeze generated JSON before launching. The runner records its SHA-256 and all
installed skill resource hashes. Evaluate unchanged Con Artist resources from
`07166bf`; do not edit resources or run author test workloads during timing.

Two cases (copy-error rollback, cancellation), baseline and skill once each:
**4 scheduled fresh sessions**, Astra medium, serial, seed 20260915, 240-second
per-cell timeout. Keep every scheduled result, stop on account limits, no retries.
No helper-adoption requirement or command-count target. Tasks explicitly require
four native tests, copied implementation binding, a reachable narrow fault, actual
native assertions/counts/exits, conditional stronger checks, original preservation
and scratch deletion. Review those obligations from original traces, not final
prose alone. Native setup failures are not successful defect detection.

```sh
python3 -B benchmarks/installer_audit_cases.py --output benchmarks/installer-audit-01-cases.json
python3 -B benchmarks/run.py --cases-file benchmarks/installer-audit-01-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260915 --timeout 240 \
  --model gpt-6-astra --effort medium --output benchmarks/local-runs/installer-audit-01
```

Compare total input (cache included once) + output and process elapsed time only
alongside reviewed task equivalence. One pair per closely related task cannot
establish a general 20–30% improvement. Distinguish missing captured evidence from
proven behavioral failure. Retain adverse results. No featured/chart promotion from
this exploratory transfer screen. Export and reconcile original traces before any
public performance claim; author replay cannot replace original model evidence.

한국어: 설치 오류·취소라는 새 작업에서 기본 모델과 스킬을 각각 1회 비교한다.
같은 실제 구현을 공유하는 저자 작성 과제 2개이며 독립 실무 검증은 아니다.
판정 기준과 입력을 먼저 고정하고 실패·시간 초과도 남긴다. 정확히 같은 일을
끝냈는지 확인한 뒤 전체 토큰·시간을 비교하며, 이번 결과만으로 일반적 성능
향상이나 20–30% 달성을 주장하거나 대표 그래프를 바꾸지 않는다.
