# Edit/test roundtrip 01 — 2026-09-20

**Promising unpromoted candidate, not an all-eight or no-skill win.** In four
fresh sessions, candidate summed tokens fall **20.51%** and process wall time
**22.11%** versus the previous skill. Both arms meet all five explicit criteria
on both variants; clean production remains unchanged. Keep the interpretation
narrow: one exposed authored task in faulty/conforming variants, n=1, fixed
order/shared host/cache, nonidentical additional checks. No exclusions/retries.

한국어: 기존 스킬 대비 합산 토큰 20.51%, 시간 22.11% 감소를 관측했다. 양쪽
모두 요구사항·범위를 충족하고 정상 코드를 보존했다. 그러나 이미 사용한 한
과제의 두 변형을 각 1회씩 측정한 개발 실험이다. 무스킬 대비 향상·8개 전체
우월성·배포 승인으로 해석하지 않는다. 후보는 아직 배포 스킬에 반영하지 않았다.

## Frozen change and costs

[Protocol](../../HOSTAGE-ROUNDTRIP-01-PROTOCOL.md), launch `eea866f`.
Original resources `3083086`; candidate changes only the dedicated-test sentence
using [the frozen transformation](../../hostage_roundtrip_candidate.py). It permits
awaiting a successful edit and running the dedicated native test command in the
same tool interaction, while retaining separate exits and failure inspection.
It does not remove tests, authorize concurrent edits/tests or bypass failed edits.
Assets and other instructions are unchanged. Candidate bodies are retained in
original tool records and tied to resource digests in [run.json](run.json).

GPT-6 Astra medium, serial, 360 seconds/cell. Fault order original/candidate,
clean candidate/original. No fresh baseline arm; earlier no-skill results are not
substituted as contemporaneous controls. Full input (cache included) plus output
tokens counted once; reasoning not added again. Whole-process time, not native
test runtime; no billing estimate or confidence interval.

| Variant | Original tokens / seconds / responses | Candidate tokens / seconds / responses |
| --- | ---: | ---: |
| Faulty | 173,886 / 112.036 / 8 | 130,183 / 104.871 / 6 |
| Conforming | 146,696 / 168.537 / 7 | 124,662 / 113.671 / 6 |
| Sum | 320,582 / 280.573 / 15 | 254,845 / 218.542 / 12 |

[Reviewed rows and arithmetic](comparison.json). The observed total is a ratio
of sums. Latency variability, differing checks and repair costs prevent attributing
the full difference to the instruction change. Exact instruction exposure and
recorded response/cumulative usage reconciliation are retained per cell; private
initial instructions/raw rollouts are not exported.

## What actually happened

All four sessions read the full asset, copy it unchanged and use ControlledCall
and OwnedTasks. No saving from usage-only reads is demonstrated here.

- Fault original: test creation, before tests, production patch and after tests
  are separate outer calls. Before: seven methods, four genuine restoration
  failures. After the one-line prepend fix: seven pass. No test repair.
- Fault candidate: creation plus before tests share stored call 28/output 33;
  patch plus after tests share call 35/output 39. Awaited edits actually succeed
  before tests start. CLI native items 6 (exit 1) and 8 (exit 0) remain separate.
  Same four real failures before, seven passes after, same production fix.
- Clean candidate: first test creation is not immediately followed by tests.
  The model then removes its generated expression
  `await self.retry(buffer, ()) if False else asyncio.sleep(0)` and replaces it
  with a genuine retry check. That repair plus native tests share call 36/output
  40; seven pass, production untouched. There is no native result for the
  intermediate suite. Its extra response and all cost are retained. No sleeps
  remain in the delivered suite. Final scope checks are chained; hashes/diffs
  separately confirm preservation, not an inferred exit for each chained check.
- Clean original: creation and tests are separate; seven pass (stored output
  40). Chained final checks are followed by another call capturing individual
  whitespace and original-file equality exits (both 0, stored output 54).
  This extra round trip contributes to the difference and is not hidden.

All suites cover actual callback entry, suppression without calling send,
receipt/item/ordinary-error identity, success retaining concurrent additions,
ordered restoration/retry for async failure, task cancellation and synchronous
callback failure, independent buffers, bounded waits and registered cleanup.
They avoid incidental backing-container or cancellation-exception identity.
Clean original additionally drives suppressed coroutines to StopIteration to
assert no suspension; candidate does not have that exact check. Other scenarios
vary in repeated references and mutable payloads. Coverage of explicit criteria
is comparable, **not identical generated work** or a universal correctness proof.

Only fault production and permitted local tests/support change. Original
requirements, AGENTS, notes, HEAD and installed resources remain unchanged. No
external discovery/installs/publishing or leftover scratch was observed. Final
answers agree with actual native outputs.

## Original evidence and separate controls

| Cell | Native CLI items | Stored output lines | Final tests |
| --- | --- | --- | --- |
| [Fault original](original/buffer-flush-fault--skill--1/) | 6, 9 | 39, 53 | 7 pass |
| [Fault candidate](candidate/buffer-flush-fault--skill--1/) | 6, 8 | 33, 39 | 7 pass |
| [Clean candidate](candidate/buffer-flush-clean--skill--1/) | 7 | 40 | 7 pass |
| [Clean original](original/buffer-flush-clean--skill--1/) | 6 | 40 | 7 pass |

Original native failures exit 1, final passes exit 0. Native and empty
copy/integrity outputs were correlated with their stored calls; no missing
native output was found. Mechanical any-output matching is screening only.
Initial exact skill body exposure is observed for each selected revision.
Every cell retains original events, selected stored records, delivered suite,
diff, metadata, source hashes, exposure, usage and review results.

[Sixteen separate author checks](author-controls.json), after all model sessions
ended, preserve originals and test disposable copies: every delivered suite
passes correct and valid container-replacement implementations, each produces
four genuine restoration assertion failures on faulty code, and the independent
six-test oracle passes every delivered production implementation. No errors or
timeouts. These are not extra model tasks, repaired original evidence or part of
the model cost. Pre-launch positive/negative/valid-alternative oracle controls
remain in run.json.

## Decision and remaining evidence

Keep as a promising isolated candidate pending another task boundary and an
edit-failure check. All observed edits succeeded: this experiment does **not**
prove the model gates testing correctly when an edit fails. Do not promote a
single favorable development comparison into a featured chart or universal
claim. Previous adverse [buffer costs](../hostage-buffer-01/README.md) and
[all-eight results](../all-eight-current-02/README.md) remain relevant. Production
skills and frozen featured charts are unchanged by this report.

한국어: 결함 수정에서는 편집→테스트를 같은 도구 호출에서 순서대로 실행해
실제 응답이 8회에서 6회로 줄었다. 정상 코드 검토에는 테스트 작성 중 자체
수정이 있었고, 기존 조건에는 최종 검사 종료 코드를 다시 확인한 비용이 있었다.
모두 그대로 포함했다. 실제 편집 실패 상황과 다른 과제에서도 검증하기 전까지
후보 상태를 유지한다. 별도 16개 검사는 모델 측정값에 합산하지 않았다.
