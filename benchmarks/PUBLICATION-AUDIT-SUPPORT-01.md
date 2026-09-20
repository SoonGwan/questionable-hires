# Existing audit support versus custom setup — 2026-09-21

Parent `730df4c`. The [discovery screen](results/con-artist-discovery-01/README.md)
retains two expensive repair paths: candidate-unknown's unloaded startup tracer
and original-known's malformed generated stronger-test source. No model used the
shipped audit helper in that screen. The discovery candidate remains rejected.

Before adding another runtime helper, this check exercises the existing `audit.py`
interface on the retained publication project's original files. No model session
is rerun, and these author checks do not replace its original observations.

## What already works

- `import_roots: ["checks"]` and listed `engine`, `bridge`, `test_engine` imports
  establish the actual native discovery module in each disposable check process.
- `precheck` asserts `test_engine.publish is bridge.refresh` and the bridge's
  `_install` global is `engine.install`. It executes explicitly in the helper's
  bootstrap, without relying on sitecustomize startup discovery. This verifies
  bindings at that point, not later fixture rebinding or execution call counts.
- `probe_replacements` supplies the complete proposed test source, keeping both
  existing method bodies/assertions. Four fresh native checks run with original
  versus appended stronger tests and correct versus omitted-replacement code.
  Existing tests pass both; the added real-byte assertion passes correct code and
  fails faulty code with actual old and expected full Unicode publication bytes.
  It also checks acknowledgment and pending-file removal.

No new runtime feature or mandatory entrypoint rule is justified by this check.
Instead, the [existing-test guide](../skills/con-artist/references/existing-tests.md)
now connects this optional same-process binding check directly to its four-check
recipe, including the limits and import-root link. The native JSON recipe already
avoids the multi-layer generated-source wrapper used in the failed model attempt;
this is an available workflow, not evidence the model will choose it.

## Validation and limits

[Regression tests](../tests/test_audit_publication_recipe.py) execute seven child
checks across three author scenarios:

| Scenario | Child checks | Observed outcome |
|---|---:|---|
| Valid complete recipe | 4 | Existing 2pass/2pass; stronger 3pass/2pass+1 byte assertion failure |
| Wrong writer binding | 1 | Reserved precheck exit6; no native tests; incomplete |
| Unterminated stronger source | 2 | Existing correct passes, correct probe import exit7; mutant checks unrun |

Original bytes/modes, exact remaining files and scratch removal are checked in
each scenario. The three tests pass on Python3.11.16 and Python3.9.6; 13 build and
two documented-probe checks also pass on Python3.11.16. The build tests execute
the packaged four-check recipe. No complete repository-suite rerun is claimed.

The stronger source is supplied as a Python raw string in the author test. This
does not prove arbitrary future generated JSON or Python syntax is valid. Invalid
probe source still incurs the preceding correct baseline and fails as incomplete;
the helper does not eliminate every repair. No timing/token savings measurement,
new model adoption evidence, chart update or broad all-eight improvement follows.
Future model confirmation needs a distinct task, not another tuned replay of this
now-exposed publication project.

한국어: 새 실행기를 추가하지 않고 기존 감사 도구의 `precheck`와 네이티브 4회
비교를 실제 파일 교체 과제에 적용했다. 정상·결함 바이트 차이를 잡고 잘못된
바인딩·문법 오류는 검증 미완료로 구분했다. 안내에서 이 기능의 사용 경로와
한계를 명확히 했으며, 이후 fixture 재바인딩이나 호출 횟수를 증명한다고 하지
않는다. 작성자 측 검사이며 모델 토큰 절감이나 이전 측정의 대체 결과가 아니다.
