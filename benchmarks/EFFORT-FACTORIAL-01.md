# Effort × skill 01 — reviewed checkpoint, 2026-09-21

Resource `35bba0a`, launch `4f47d5b`, [frozen protocol](EFFORT-FACTORIAL-01-PROTOCOL.md).
All eight scheduled sessions completed, without timeout, account-limit stop,
replacement or retry. Actual stored turn contexts identify GPT-6 Astra and the
requested low/medium effort in every cell. CLI token totals reconcile with original
stored cumulative and response records. **Task/artifact review is complete: all
eight meet the four functional/artifact criteria, but both SQLite baselines violate
the project-only scope. No efficiency promotion or default change.**

[All retained observations](results/effort-factorial-01/README.md) include source
identities, native author preflight, original tool records, usage, exposure and
capture correspondence. Private initial instruction text is not exported.

| Task | Effort | Arm | Input + output tokens | Process seconds |
| --- | --- | --- | ---: | ---: |
| SQLite audit | low | baseline | 65,898 | 65.410 |
| SQLite audit | low | current | 155,472 | 80.988 |
| SQLite audit | medium | baseline | 83,627 | 72.372 |
| SQLite audit | medium | current | 115,907 | 54.873 |
| Refresh ownership | low | baseline | 84,039 | 92.446 |
| Refresh ownership | low | current | 162,860 | 94.828 |
| Refresh ownership | medium | baseline | 86,398 | 112.849 |
| Refresh ownership | medium | current | 119,546 | 106.448 |

Cache is included once in input; reasoning output is not added a second time.
These are two extensively exposed authored tasks, n=1 per condition, serial on
one shared host/cache. Summed work is descriptive accounting, not a task-weighted
effect estimate or an uncertainty interval. At both effort levels the current
skill uses more tokens on each task. Current-low versus current-medium also uses
more tokens on both; SQLite is slower while Refresh is faster. Lower effort is
not a demonstrated remedy for this bundle's cost problem.

## Reviewed outcomes and unequal work

| Task / effort | Baseline criteria | Current criteria | Baseline scope | Current scope |
| --- | --- | --- | --- | --- |
| SQLite / low | 4/4 | 4/4 | fail: parent search | pass |
| SQLite / medium | 4/4 | 4/4 | fail: parent search | pass |
| Refresh / low | 4/4 | 4/4 | pass | pass |
| Refresh / medium | 4/4 | 4/4 | pass | pass |

Criteria retain the frozen task definitions. The separate project-only boundary
is mandatory:4/4SQLite criteria must not be presented as full-task success for
the baselines. There are two tasks at n=1 per configuration, not eight independent
tasks. Neither the scope difference nor these scores prove general superiority.

SQLite: all four inspect actual sources, verify the test-to-endpoint-to-writer
binding in the process executing the checks, and execute existing tests on both
normal and missing-commit code. The original tests pass2/2on both versions. The
same stronger native assertion passes normal code and fails the faulty version
for a missing binary row through a fresh SQLite connection, retaining the prior
row. Low-current strengthens both binary and empty-upload tests (2methods per
probe); the other arms use one binary-row probe. Baselines additionally trace
actual writer calls; medium baseline also traces reached close/return lines.
Required outcome is met, but execution detail/extra evidence is unequal.

Refresh: all four apply exactly the latest-generation guard in `finally`, without
serialization, suppression or cancellation of other calls. Delivered native tests
cover both success orders, stale failure/cancellation while latest is unresolved,
latest failure/cancellation and retry, synchronous failure, result/error identity,
prior-value retention and instance isolation. Callback-start and result waits are
bounded, cleanup is owned and bounded, and no timing sleeps are used. Review
examined actual test bodies, not just method counts. Medium baseline delivers
7methods, low baseline5, medium current5and low current8; subtests cover multiple
transitions, so method counts are not a quality ranking.

- Both SQLite baseline commands search `find .. -name AGENTS.md`, outside the
  explicit project-only boundary. Retain these scope failures; do not call them
  equal-scope controls or exclude them to improve a headline.
- Low-current SQLite invokes the audit helper with probe fields at batch top
  level, receives an input-contract error, reads the batch guide and recovers.
  The error/recovery cost stays included. Medium-current uses the helper too.
  The subsequent [route/diagnostic correction](AUDIT-BATCH-PROBE-ROUTING-01.md)
  is unmeasured here; no original result is attributed to the newer instructions.
- Both Refresh skill arms copy/use `controlled_call.py`, retain before-fix
  failures and after-fix passes. Baselines use their own test support and only
  run their completed fix (low baseline repeats that same suite). Current medium
  reports4failures before/5methods pass after; current low reports5failures
  before/8methods pass after. These are original executions, not author replay.
- Installed skill manifests match the pinned resource and remain unchanged.
  All original SQLite file contents survive; Refresh changes `preview.py` while
  requirements/owner notes survive. The [author review](results/effort-factorial-01/author-review.json)
  verifies exact allowed final inventory, expected production bytes and original
  file modes. Copies of the controlled-callback asset match pinned bytes. No
  owned audit scratch remains. Final state cannot prove every transient action.

## Capture limitations retained

SQLite low baseline loses a1,360-character output prefix in CLI display, low
current134characters, medium baseline3,478characters. Matching stored outputs
retain those prefixes. Medium-current's actual source/native-guide read appears
only in original tool output at stored line20, not the CLI command list. Thus the
missing CLI item is not treated as missing source inspection or rerun.

Three empty successful shell outputs in Refresh medium-current and two identical
successful test outputs in Refresh low-baseline are not uniquely mapped by the
existing content matcher. All original records remain; this is an ambiguous
correspondence, not proof of omitted execution. Original call/output review
resolves their roles: medium-current's copy/test block is at call line28/output33,
and ordered `Promise.allSettled` comparison/diff checks at call45/output50.
Low-baseline's first test is in call27/output31; its second is check0in the ordered
call35/output39. The generic matcher remains honestly ambiguous; its artifacts
are not rewritten to imply unique content matches.

Exact skill bodies are observed in tool outputs for all four current sessions;
neither installed body's exact text is detected in baseline records. The scanner
does not prove absence of every skill-related instruction or complete initial
context, and file reads alone do not establish why the model made a decision.

## Separate post-timing sensitivity checks

Fresh author copies run each delivered Refresh suite against its delivered fix
and the original defective source. All delivered versions pass; the originals
produce real assertion failures (medium baseline5, medium current4, low current5,
low baseline6, including subtest failures). No setup errors or runtime warnings.
This confirms sensitivity of the retained suites, **not** that baselines performed
before-fix checks. The author copies are removed; measured workspaces are unchanged.

## Decision

Descriptive two-task sums: low-current versus low-baseline+112.31%tokens/+11.38%time;
medium-current versus medium-baseline+38.48%tokens/−12.90%time. Current-low versus
current-medium+35.20%tokens/+8.99%time. Unequal verification and baseline scope
failures prevent equal-work efficiency attribution. These sums are not the
featured chart's task-ratio statistic and are not release acceptance.

Do not change default effort or promote this screen. Keep the narrow subsequent
input-contract correction, whose model benefit remains unknown. Do not rerun the
same exposed tasks until favorable; further model work requires a distinct
supported mechanism and appropriate controls. The all-eight, similar/lower-cost
objective and independent generalization remain unproven.

## Preparation checks

Checkout runner controls5/5; fresh source archive4pass/1historical skip. Actual
fixture preflight: both public imports pass, original SQLite receipt tests survive
the lost commit while the stronger assertion fails specifically for missing rows,
and the asynchronous original/fault controls produce their expected native pass/
failure. These author checks precede model execution and do not score the models.

한국어:8회 상세 검토를 마쳤다. 기능·결과물 기준은 모두 충족했지만 SQLite의
무스킬2회는 상위 경로 검색으로 작업 범위를 위반했다. 실제 테스트·수정량·추가
검사 차이와 별도 작성자 재검사를 구분했다. 낮은 추론 강도도 토큰 증가를 해결하지
못했으므로 기본 설정과 대표 그래프는 유지하며 전체 성능 향상으로 주장하지 않는다.
