# Receipt comparison reference disclosure

2026-09-15, parent `98613b6`. Documentation/interface change only.

The [all-eight screen](results/lean-screen-01/README.md) showed current Receipt
reading 381 helper source lines after the routine interface. The lean entry used
a focused source search instead and had lower recorded cost on that one task;
that does not prove the guide caused either behavior.

The [routine guide](../skills/receipt/references/existing-fix.md) now routes
startup-hook semantics, detailed exit interpretation and process/guard boundaries
to [conditional details](../skills/receipt/references/comparison-details.md).
Recipes, selection rules, native module invocation, same-process imports, guard
authorization and exclusions, essential status interpretation and cleanup limits
stay in the routine guide. Reading implementation remains appropriate for a
concrete trust, adaptation or diagnosis question. No blanket prohibition on source
inspection or mandatory extra setup pass is introduced.

Both existing committed/uncommitted command examples remain unchanged. Entry
instructions, selection metadata, executable helper and assets are unchanged;
the unpromoted all-eight lean rewrite is not installed.

## Local verification

- `python3 -B -m unittest discover -s tests -p 'test_receipt*.py'`:
  **95 tests passed**, 33.500 s. Includes executing both literal documented examples,
  actual before-failure/after-pass assertions, native import provenance, hook
  compatibility, original preservation, cleanup and adverse helper controls.
  The expected hook-error test prints `RuntimeError: original configured hook`;
  it is not a missing/ignored suite failure.
- `python3 -B -m unittest tests.test_install`: **20 passed**, 1.782 s.
- Skill Creator's `quick_validate.py skills/receipt`, repository validation and
  featured English/Korean synchronization check pass.

Routine guide size: 7,898 → 6,354 UTF-8 bytes (19.55% smaller). Conditional details
add 4,804 bytes: the combined documentation is **11,158 bytes, larger than before**.
This is progressive disclosure, not a smaller bundle, measured token savings or a
whole-task performance gain. No new model session or favorable rerun. Existing
results and charts remain tied to their measured revisions.

Next validation needs an independently specified comparison task and actual
guide/source-loading observations; documentation size alone cannot justify promotion
of the lean entry or a performance claim.

한국어: Receipt의 일반 실행 안내와 조건부 상세 설명을 분리했다. 기본 안내는
19.55% 짧아졌지만 전체 문서량은 늘었으며, 모델 토큰 절감률이 아니다. 실행 코드와
진입 지침은 유지했고 Receipt 95개·설치 20개 검사를 통과했다. 기존 실패 근거와
그래프는 그대로 두며, 실제 읽기 동작과 작업 비용은 새 과제에서 검증해야 한다.
