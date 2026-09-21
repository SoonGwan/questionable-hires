# Audit proposal01 — scope distinction observed, broad efficiency unproven

2026-09-21. Frozen launch `666fb94`; prior resource `740948e`, current `e17e13d`.
[Protocol](AUDIT-PROPOSAL-01-PROTOCOL.md), [all four attempts](results/audit-proposal-01/),
[structured review](results/audit-proposal-01/comparison.json).

The entry change distinguishes an assertion **proposal** from a verified repair.
Helpers were identical. Two related requests reuse the already-observed cachetools
development fixture; this is not independent holdout evidence. GPT-6 Astra medium,
n=1, serial fixed order: proposal/prior→current, verified/current→prior. All four
scheduled attempts completed; no timeouts, retries or excluded attempts.

| Request | Resource | Total tokens | Wall seconds | Unittest processes | Criteria |
| --- | --- | ---: | ---: | ---: | ---: |
| Proposal only | Prior | 127,347 | 123.017 | 20 | 5/5 |
| Proposal only | Current | 105,116 | 112.584 | 10 | 5/5 |
| Verified assertions | Prior | 88,723 | 100.776 | 19 | 6/6 |
| Verified assertions | Current | 91,739 | 97.408 | 18 | 6/6 |

Proposal pair: current uses17.46% fewer tokens and8.48% less time. Verified pair:
current uses3.40% **more** tokens and3.34% less time. These are individual observed
pairs, not significant estimates or a universal improvement. Full input+output
counts cached input once; all discovery, optional execution and trace costs remain
included. Unittest counts are not all subprocesses, shell calls or unique tests.

## Reviewed behavior

All four established two correct-code passes plus the same eight isolated fault
outcomes with unchanged selected test bodies:

| Fault | Ordinary test | Weighted test |
| --- | --- | --- |
| No read recency refresh | Behavioral KeyError at line26 | Survives |
| No overwrite recency refresh | Survives | Survives |
| Most-recent eviction | Behavioral KeyError at line19 | Survives |
| Ignored size callback | Survives | AssertionError `3 != 1` at line48 |

Every answer interpreted the KeyErrors as behavioral detections, not import/setup
failures, and reused the two normal observations explicitly. Mutations were
confined to LRUCache. Actual native outputs, not answer claims alone, establish
these observations. The unweighted selector never supplies a custom size callback;
its survival does not mean it violates its own unweighted contract. The protocol's
shorthand “default size-callback behavior” denotes this absent coverage, not an
existing default-sizing defect. Supplemental callback assertions extend coverage.

On proposal-only, prior ran the required10 processes plus8 stronger-assertion
processes and2 extra fault traces. Current ran only the required10, with in-process
tracing, gave a concrete overwrite assertion and a read variant, and explicitly
labeled them unexecuted proposals. It identified custom sizing as already covered
by the weighted test. Both satisfy the frozen proposal criteria; prior's optional
checks are not scored as a quality failure or removed from its cost.

On verified assertions, both covered all five surviving combinations with genuine
normal passes and fault-specific assertion failures. Current grouped default and
weighted overwrite into subtests:8 extra processes. Prior separated those methods
and shared one weighted read assertion across read/MRU faults:9 extra processes.
The prior shared normal observation was identified, not counted as repeated work.
Neither arm substituted an unexecuted suggestion for required verification.

Three attempts used `sitecustomize` tracing of executing tests and copied class
bindings. Verified/prior appended import/binding checks to the **copied test module**;
it did not edit its test bodies or the original file. That same native process ran
the selected methods; the append did not replace their assertions. This difference
is retained rather than describing all copied module bytes as unchanged.

All original project file bytes/modes, HEAD and installed resources were unchanged;
owned copies/instrumentation were removed. Final delivery contains only the eight
initial project files. Pre-collection index entries match the initial tree; no
pre-session binary index exists to prove byte-identical index preservation.

## Exposure, capture and limits

All four skill bodies appeared in recorded initial messages and were read again.
No session invoked the optional audit helper or read its guide. This experiment
therefore concerns the entry's scope boundary, not the helper-cache optimization.

Of17 shell outputs,15 exactly match original stored output. Two current source
reads are truncated in original storage and unmatched; one uses a different banner
than the matcher's sentinel, so its `truncated: false` field is not completeness
evidence. All actual native audit outputs match exactly and retain the relevant
passes, assertion failures, provenance and cleanup observations. No author replay
was used to supply missing original evidence. Export includes redacted original
tool records and exposure/usage metadata, not raw private initial instructions.
The privacy scan is limited detection, not a security certificate.

This is a development regression comparison: two requests on one known fixture,
n=1, shared host/cache, unblinded review, unequal optional work and differing trace
strategies. Fewer optional tests are less work, not faster execution of identical
work. The result supports retaining the narrower scope instruction provisionally;
it does not prove causality, generalize to independent projects, establish all-eight
efficiency or authorize release. Featured charts remain frozen. No further prompt
change was selected from this run.

한국어: 제안 과제에서는 요청한 감사 결과를 유지하며 테스트 실행이20회에서10회로
줄었다. 토큰17.46%, 시간8.48% 감소가 관측됐다. 실제 입증 과제에서는 정상·결함
양쪽 검증을 유지했지만 토큰은3.40% 증가했고 시간은3.34% 줄었다. 기존 사례를
재사용한 단일 비교이므로 일반적인 성능 향상이나 전체8개 스킬의 우위로 확대하지
않는다. 원본 출력 일부 잘림과 작업량 차이도 보존하며 대표 그래프는 바꾸지 않는다.
