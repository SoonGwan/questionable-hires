# Proportional audit tooling — 2026-09-15 KST

Parent `03c5963`. The [installer transfer](results/installer-audit-01/README.md)
observed 75–97% more skill tokens, helper source inspection and repeated recipes,
despite valid native detection. The previous entry told compatible Python audits
to use the helper instead of rebuilding orchestration, with simpler approaches as
an exception. That can make compatibility look like sufficient reason to adopt it.

Change only that routing bullet: small self-contained audits use native runners
in isolated copies or valid substitutions. Choose the helper when its bounded
processes, selected-input integrity checks or shared-baseline batching remove
needed orchestration. Compatibility alone no longer requires helper/guide uptake.
All assertion, binding, isolation, scope and preservation obligations remain;
supported helper features and implementation are unchanged. This does not forbid
tools, tracing, legitimate trust review or project-specific facilities.

Hypothesis, not demonstrated improvement: avoid tool adoption that adds more work
than it removes. Skill Creator informed the narrow outcome-based routing; no
additional universal checklist or installer-specific answer was added.

One changed-candidate screen uses the unchanged two installer tasks, fresh baseline
and skill once each, serial Astra medium, seed 20260915, timeout 240 seconds. Same
frozen JSON hash as transfer 01; four cells, no retries or favorable-run selection.
This is an exposed development set, not a holdout. Retain all original observations
and review task equivalence, native assertions, provenance, preservation and cost.
Previous transfer stays frozen. Do not promote a single favorable comparison.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/installer-audit-01-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260915 --timeout 240 \
  --model gpt-6-astra --effort medium --output benchmarks/local-runs/installer-native-02
```

한국어: 작은 Python 감사에서도 도우미를 우선 도입하던 안내를 바꿨다. 필요한
격리·무결성·배치 처리를 줄여주는 경우에만 선택하고, 단순 작업은 기존 테스트
실행기를 직접 사용한다. 실제 검증과 원본 보존은 줄이지 않는다. 모델 효과는
아직 가설이며 같은 개발 과제의 새 비교를 통해 확인한다. 기존 불리한 결과를
덮어쓰거나 이번 비교를 독립 검증으로 포장하지 않는다.
