# Con Artist repository audit 01 — mixed whole-task result

2026-09-20. Launch `3ca7b4d`; installed resources `ee51757`; task implementation
and four tests are unchanged repository snapshots from `716493b`.
[Frozen protocol](../../CON-ARTIST-REPOSITORY-01-PROTOCOL.md),
[case/preflight](../../CON-ARTIST-REPOSITORY-CASE.md),
[full reviewed rows](comparison.json).

Two fresh serial GPT-6 Astra medium sessions, baseline then current, n=1, shared
host/cache. This is our own repository with a thread-authored audit request, not
an independent external project or held-out evaluation. No scheduled attempt
was replaced or excluded. The baseline's within-session repair remains included.

| Condition | Input + output tokens | Wall seconds | Recorded responses | Task / scope |
| --- | ---: | ---: | ---: | --- |
| No skill | 100,455 | 133.236 | 5 | Pass / pass |
| Current Con Artist | 111,962 | 91.291 | 5 | Pass / pass |

Current: **+11.45% tokens, −31.48% time**. Full input includes cached input once;
reasoning is not added again to output. This is descriptive, not a causal speedup:
baseline repaired an extra cleanup assertion and repeated its correct-code run;
the arms used different valid faults, copy contents and instrumentation. Neither
invoked the installed context collector. This does **not** measure the recent
line-index optimization, prove broad efficiency, or satisfy the all-eight goal.

## Original execution and scoring

Both arms satisfy all five frozen criteria: unchanged native correct/faulty
four-test execution, meaningful cross-call cache reuse, accurate assertion/coverage
explanation, copied implementation identity/binding and native exits, original
preservation and project-local scratch/copy removal. No production/test fix remains.

- Baseline introduced one module-level cache keyed by relative path. Correct
  tests pass; mutant has three passes and one assertion failure, native exit 1.
  `test_no_stale_spans_after_new_invocation`, line 86, observes `('f0', 'f0')`
  instead of `('old', 'changed')`: a previous test's different project supplied
  `module.py`. The answer correctly distinguishes this order-dependent detection
  from a dedicated cross-project assertion. Binding/collect filename/hash checks
  run in a **separate precheck process**, not inside native unittest.
- Current introduced a module-level dictionary keyed by resolved project root,
  retaining each root's cache across calls. Correct tests pass; mutant has three
  passes and one assertion failure, native exit 1. The same line 86 observes
  `('old', 'old')` instead of `('old', 'changed')`. Copied `sitecustomize.py` plus
  child-only `PYTHONPATH` installs tracing in the actual native unittest process;
  module binding/hash, skipped reread, unchanged excerpt/hash are visible. It
  targets project `skills/con-artist/scripts/context.py`, not installed `.agents`.
- Both use the required `python3 -B -m unittest discover -s tests -p
  test_context_line_index.py -v`; native children have copy-local absolute
  `TMPDIR`. Current's trace shows actual temporary roots beneath `.test-tmp`.
  Tests are byte-identical to originals. Baseline copies the entire project;
  current copies source/test/AGENTS plus its observation hook. Both remove owned
  roots in `finally` and verify unchanged original contents/modes, including
  owner notes/cache. Mechanical review finds no original changes or extra files.

Baseline's first correct run passed all four tests, then an **additional**
scratch-empty assertion failed. The answer attributes contents to the launcher;
the original output does not list those contents, so that attribution is not
independently established. Its `finally` removed the copy and verified originals.
The next command drops that extra emptiness assertion, repeats correct tests,
runs the mutant and removes the entire owned directory. All this cost is retained.
This is not a fixture assertion failure or permission to exclude the attempt.
Native runs in both arms emit Xcode launcher diagnostics but reach actual tests.

Current trace labels line events as “assertion reached,” including mutant line 87
after line 86 fails. A trace line event is **not proof an assertion completed**;
we credit neither execution nor an independent detection to the subsequent hash
assertion. Both final answers correctly withhold that claim. No new author replay
was used to replace original outcomes. The separately labelled author preflight
in `run.json` is setup evidence only.

## Capture and exposure

Selected command-correlated original tool records are included; raw private initial
instructions are not. Exposure metadata confirms current Con Artist's body in
initial context, baseline no skill body. Reading SKILL.md later is not new exposure.

- Baseline CLI `item_4` omits inventory/source/test-hash prefixes retained at
  original record line 30; `item_6` omits correct-source/test hashes retained at
  original line 39. Binding/native assertions/exits remain in both captures.
- Current CLI `item_6` omits the leading baseline PHASE/source hash retained at
  original line 39; in-process binding repeats the same hash. Other command
  outputs match under normalization. Original execution outputs are not truncated.

No chart, featured pointer, release readiness or general performance claim changes.
Preserve this mixed result; do not tune/repeat this exposed case until favorable.

## 한국어 요약

실제 저장소의 코드·테스트를 그대로 사용한 감사 과제다. 외부 독립 평가나
미공개 과제는 아니다. 무스킬 100,455토큰·133.236초, 스킬
111,962토큰·91.291초로 **토큰 11.45% 증가 / 시간 31.48% 감소**였다.
양쪽 모두 다섯 평가 기준과 원본 보존·정리를 충족했다.

무스킬은 프로젝트 간 공유 캐시, 스킬은 같은 프로젝트의 호출 간 공유 캐시를
주입했다. 둘 다 원본 테스트 네 개는 통과하고 결함에서는 실제 값 불일치가
발생했다. 스킬 쪽은 실제 테스트 프로세스 내부에서 소스 연결과 오래된 결과를
추적했다. 후속 해시 검사는 독립적인 결함 탐지로 인정하지 않는다.

무스킬의 추가 임시폴더 검사 실패와 재실행 비용도 포함했다. 이 차이와 다른
결함·복사·추적 방식 때문에 시간 감소를 스킬만의 효과로 단정할 수 없다.
설치된 탐색 도구는 양쪽 모두 사용하지 않아 내부 최적화의 모델 성능 측정도
아니다. 초기 비공개 지시는 공개하지 않으며 캡처 앞부분 누락은 원본 기록으로
확인했다. 전체 8개 성능 개선 목표는 미달이며 대표 차트나 배포 판단은 바꾸지 않는다.
