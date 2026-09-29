# Necromancer retained matrix01 — candidate API gate, 2026-09-27

Parent `8da1825f`. Separate unadopted
[candidate](candidates/necromancer-retained-matrix/skills/necromancer/SKILL.md)
starts from frozen inline candidate `80c06e2e`; ordinary eight skills, previous
model inputs, output and featured charts remain unchanged.

The [native retained-outcome prototype](CALL-MATRIX-RETAINED-01.md) is copied
byte-for-byte into this skill's actual `scripts/call_matrix.py`. The entrypoint
shows `retain=True` for requested per-case actual values and prints ordered
observations after completeness checks. It distinguishes summary-only use and
required tests; it does not require a particular tool, reduce case coverage,
predict counts, prefill solver values or override source binding/history duties.
The reference explains version3 opted-in observations, unchanged default v2,
partial-prefix/error semantics and the risk of larger output. Implementation
inspection remains appropriate when adaptation or verification needs it.

[Retained control](results/necromancer-retained-matrix-native-01/control.py)
loads the **candidate's actual installed-layout API path**, rather than the
standalone prototype. It cold-imports the local pinned public upstream package
with genuinely generated metadata, binds actual Retry.is_retry independently
for each variant, and restores the original method. Fifteen actual package
calls produce the expected current/A/B vectors and mismatch0/1/1 summaries.
Six boundary controls cover matching returns/exceptions/mismatches, unsupported
return partial-prefix stop/no replay, input mutation, default v2, invalid option
before callbacks, and typed tuple/list values.

[Original native output](results/necromancer-retained-matrix-native-01/result.json),
[Git-free archive result](results/necromancer-retained-matrix-native-01/archive-verification.json),
and [candidate/control hashes](results/necromancer-retained-matrix-native-01/identities.json)
retain actual execution. Each subprocess has parent30s bound. The source clone
is separate full-history upstream; the project archive lacks Git metadata.
Both runs preserve original tracked source, generated metadata, callback binding
and explicit input. Skill frontmatter validation also passes. No models called.
These are reused development controls, not independent holdout evidence.

This function change addresses missing requested passing observations and the
[previous invoice's duplicate calls](NECROMANCER-INLINE-MATRIX-01-REVIEW.md).
It does not repair or explain away the [adverse urllib3 nonselection](URLLIB3-INLINE-TRANSFER-02-REVIEW.md).
Native ability is not actual model selection, lower whole-task tokens/time,
all8 quality improvement, adoption or a completed next release. A prospective
model comparison must freeze this materially changed resource before execution,
retain every attempt and complete scope, inspect actual helper invocation and
requested observations, and reject adverse results. Do not run an unchanged
resource repeatedly until favorable or reuse previous timings as new evidence.

한국어: 새 미채택 후보에 첫 호출의 실제 값 보존 기능을 연결했다. 후보 자체의
실제 API 경로로 urllib3 15개 호출·경계6개 검사를 수행했고 원본 소스·생성 파일·
바인딩·입력을 보존했다. 저장소와 Git 없는 아카이브에서 통과했으며 모델0회다.
이전 중복 호출을 줄일 수 있는 기능이지만 모델의 선택·전체 비용 절감·전체8개
품질 개선은 미입증이다. 기존 기본 스킬·고정 후보·불리한 결과를 바꾸지 않는다.
