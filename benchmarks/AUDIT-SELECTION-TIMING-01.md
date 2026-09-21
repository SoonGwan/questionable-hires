# Native batch timing screen — 2026-09-21

This measures the [non-adjacent baseline reuse change](AUDIT-SELECTION-REUSE-02.md),
**not an Astra session, token reduction or all-eight improvement**.
Frozen before helper `51a4f5a`, after `b1875a0`; frozen author probe `b1875a0`.
[Runner](time_audit_selection_reuse.py), [pre-execution schedule and source hashes](results/audit-selection-timing-01/manifest.json),
[summary](results/audit-selection-timing-01/summary.json). All18 original cells are
retained alongside the manifest, with native output, counts, results and timings.

Three authored cases, three repeats per arm. Each repeat reverses the previous
pair order; case order is fixed. Serial on the same host, no warmup or exclusions,
no failed-cell replacements. Python3.9.6. Timer includes frozen helper import,
fixture setup, all native checks, validation and cleanup. It excludes initial
Python process startup, resource materialization and JSON export. The inner probe's
execution-count-only limitation describes that probe, not the enclosing timer.

## All cases, mean and observed range

| Case | Before seconds: mean [min,max] | After seconds: mean [min,max] | Change in mean |
| --- | ---: | ---: | ---: |
| Adjacent control A-A-B | 0.2252 [0.2241,0.2269] | 0.2208 [0.2199,0.2221] | −2.0% |
| Revisited A-B-A | 0.2684 [0.2622,0.2761] | 0.2362 [0.2295,0.2489] | −12.0% |
| Eight alternating selections | 0.7080 [0.6956,0.7266] | 0.4525 [0.4472,0.4604] | −36.1% |

Changes are ratios of arm means, not confidence intervals or paired significance
tests. The control performs the same5 check processes in both arms: its small
timing difference does not establish an optimization benefit. Revisited selection
performs6→5 checks; eight alternating selections perform16→10. All mutant checks
remain, with the same acknowledgment-survival/stored-value-failure assertions.
Every individual check reports one native test. No timeout, truncation, changed
original or leftover owned scratch is reported.

The largest measured mean saving is approximately **0.256 seconds**, not a large
end-to-end development-time saving. Small native examples can be dominated by
interpreter/process overhead. Shared machine/cache effects, three repetitions,
author-selected cases and cached normal observations limit generalization.
The alternating recipe deliberately favors the implemented reuse opportunity;
its frequency in real tasks is unknown. No time should be extrapolated to model
reasoning, required discovery, fresh external-state checks or token cost.

The artifact test requires all scheduled cells exactly once, verifies source
identities against the manifest, reconciles native outcomes/counts and recomputes
the complete summary. Malformed/missing/duplicate cells cannot produce a valid
summary. This is not independent adjudication of all helper behavior or platform
support. Existing regression tests cover invalidation and reference integrity.

Production code is unchanged in this timing checkpoint. Do not replace featured
model graphs with these microbenchmark percentages. The next relevant evidence
would be a fresh developer-task comparison including the cost and actual choice
to use this batch workflow, not repeated timing until a target percentage appears.

한국어: 동일한 세 예제를 수정 전후 각각3회 실행했다.8회 교차 예제는 평균
0.708초→0.452초로36.1% 줄었지만 절대 절감은 약0.256초다. 변형 검사는 모두
유지됐다. 이는 작은 도우미 실행 측정이며 모델 전체 속도·토큰 절감률이 아니다.
대조 예제와 편차도 공개하고 대표 모델 그래프는 그대로 둔다.
