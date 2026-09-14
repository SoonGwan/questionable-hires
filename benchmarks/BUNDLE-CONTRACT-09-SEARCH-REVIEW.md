# Checkpoint 09 search QA controls — 2026-09-14

Partial review of launch `3a7d972`, resources `9071a1c`;
[whole-run intake](BUNDLE-CONTRACT-09-INTAKE.md). Four original cells and their
retained tests are reviewed here, not the remaining checkpoint obligations.

## Original evidence

Both search-order sessions capture two native test names, the expected reversed
completion value AssertionError and a passing normal-order control. Both create
overlapping requests against actual Search, release them explicitly, bound waits
and clean up owned tasks. Neither requires a particular display while the latest
request is pending, consistent with that task's explicit contract.

Protected-search baseline captures four passes, skill three. Both inspect the
original generation guard and verify newer-first, older-first while newer remains
pending, and retained existing display. No production source changes occur. The
skill adds a single-request retention witness; baseline separately checks an
initially empty display. Method counts do not establish a coverage ranking.

All original native counts/decisive assertions are present in these four captures.
Skill's empty support-copy output is ordinary, not a missing-test-output gap.
Both skill assets are byte-identical to the frozen ControlledFetch file. Reviewed
retained source inventories contain only original files plus local tests/support
and, for order baseline, a saved duplicate test log. Original production and
requirements bytes are unchanged. Semicolon-separated final Git commands still
must not be interpreted using only the last shell exit.

## Separate controls

[Replay script](replay_bundle_contract_09_search.py) executes unchanged retained
tests in disposable copies beneath the local run, replacing only search.py.
The [full report](results/bundle-contract-09-search-controls/author-replay.json)
preserves original native outputs, original source hashes, redacted retained text,
replacement implementations, commands and actual failures. No model reruns.

| Contract | Implementation | Both baseline and skill tests |
| --- | --- | --- |
| Final latest result; intermediate unspecified | Original stale overwrite | Reject with actual value AssertionError |
| Same | Generation guard retaining earlier display | Accept |
| Same | Older result allowed only before latest completes | Accept |
| Retain existing display while latest pending | Original generation guard | Accept |
| Same | Older result shown while latest still pending | Reject with actual value AssertionError |
| Same | Clear existing display at request start | Reject with actual value AssertionError |

All **12/12** outcomes match. Native counts remain two for order and four/three
for protected; no outer timeouts or changed tests/support. All retained project
inventories remain unchanged. The same intermediate-display implementation is
correctly accepted or rejected according to the different task contracts, not a
universal test preference. These controls establish bounded artifact behavior,
not exhaustive correctness or a general gain over baseline.

The first author report contained a local workspace path in baseline's saved log.
It was moved to local raw storage before publication. Export redaction was added,
and the same twelve author controls ran again unchanged, all matching. Hashes
continue to identify original bytes; redacted exported text is not byte-identical
to that log. The original private artifact and all model runs remain untouched.

| Pair | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| Search order | 100,683 / 70.250 | 72,247 / 65.292 |
| Protected search | 99,291 / 67.149 | 71,686 / 62.313 |

Both pairs record lower skill cost while meeting the reviewed obligations, but
different artifacts/witnesses, exposed tasks, n=1 and shared host/cache prevent
causal or general efficiency claims. Other checkpoint regressions and the form
output gap remain. No featured or historical graph changes.

## 한국어

검색 QA 4세션의 원본 테스트 결과와 별도 대조 12회를 확인했다. 두 모델 모두
오래된 응답의 덮어쓰기 결함을 잡고 정상 구현을 통과시켰다. 중간 표시를
허용한 과제에서는 오래된 중간 결과도 허용하고, 기존 표시 유지가 요구된
과제에서는 같은 동작을 결함으로 잡았다. 원본 코드는 변경되지 않았다.

두 과제 모두 스킬의 관측 비용은 낮지만 추가 파일·검증 사례가 다르고 각
조건 1회라 일반화하지 않는다. 다른 과제의 비용 증가와 폼 출력 누락도 남는다.
공개 전 로그의 로컬 경로를 발견해 첫 작성자 결과는 로컬에 보존하고 공개
경로 가림 후 동일 대조를 다시 확인했다. 전체 평가 검토와 그래프 갱신은 남았다.
