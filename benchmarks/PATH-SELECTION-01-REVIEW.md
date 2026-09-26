# Path-selection transfer01 — 2026-09-27

Unchanged Exorcist resource from **`9fdee801`**, frozen inputs/launch **`3ff3fa85`**.
[Protocol](PATH-SELECTION-01-PROTOCOL.md),
[all four attempts](results/path-selection-01/comparison.json),
[original response arithmetic](results/path-selection-01/input-cost-analysis.json).
All four fresh serial Astra medium sessions completed, without timeout, account
stop or replacement. Original persisted sessions match their CLI thread IDs and
all per-response counters reconcile. Each session has six recorded responses.
Whole-task tokens are input+output, cached input included once; process wall time
excludes author preparation. No billing or causal latency estimate follows.

| Task | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| Relative filename cache |103,477|104,892|117.937|80.952|
| Retained reader binding |100,472|110,076|112.912|106.611|
| Sum |203,949|214,968|230.849|187.563|

Summed tokens **+5.40%**, time **−18.75%**. Both tasks take less recorded time but
more tokens; neither improves both. These authored related fixtures have n=1,
grouped execution order and a shared host/cache. They are not independent external
validation or all-eight coverage. No broad efficiency statement or skill adoption.

## Original task outcomes

All four original native tests execute the same three test identities: single
root and other filename pass; switching roots fails with actual111 versus
expected222. This is the requested defect reproduction, not three passing tests.
The native assertion aborts before switching back; each original model probe
separately exercises alpha→beta→alpha and a fresh beta client through the actual
supplied implementation. No supplied source, tests, configuration or data changed.

In both relative-cache conditions, wrappers delegate to the actual cached loader
and `Path.read_text`. The client selects beta correctly but passes the unchanged
relative filename. The beta request and fresh beta client return alpha's111
without a loader file read. Clearing only the in-process cache while retaining
the beta client/root/filename makes the loader read beta and return222. Both
normal controls remain. Both diagnoses identify the root missing from the cache
key and recommend a root-qualified path without implementing a fix.

In both retained-binding conditions, delegating loader/open/stream-read wrappers
show beta requests passing an alpha path and reading alpha again. A fresh beta
client reads beta and returns222. Both retain settings/other-file controls and
the return to alpha; both identify construction-time `_read_root` surviving
`select_root`, and recommend using current `root` without implementing a fix.
These observations distinguish stale path selection from cached return content.

Probe source and retained JSON were reviewed against actual calls, ordering and
outputs, not just wrapper exits. Wrappers observe the application's original
functions; they are not replacement application simulations. Both conditions
deliver rerunnable probes, JSON linking requests/loader inputs/reads/results,
corrective directions and explicit production uncertainty. The scoped requested
outcomes are supported, without a comparative quality advantage.

## Evidence and limits

The [artifact review](results/path-selection-01/artifact-review.json) compares all
eight supplied files per cell against fixture digests, directly recorded pre-model
regular-file modes and final artifacts. Bytes/modes match; captured initial versus
before-collector index bytes/modes match and installed resources have no changed
paths. Frozen runner, fixture, launch and all eight resource hashes were rechecked.
These are final-state observations, not proof of every transient operation or
all Git metadata. Raw initial inventories and full private sessions stay local.

Actual original skill exposure is recorded per cell. Both skill sessions receive
the exact Exorcist body before the first tool and reread it later. Neither baseline
has an exact hire-body match in recorded initial messages/tool outputs. Missing
matches do not prove absent unrecorded context or disable enforcement. No private
instructions are published. Existing [context-exposure review](CONTEXT-EXPOSURE-01.md)
already cautions against removing host-required reads to optimize this observation.

Relative-cache baseline's probe output is empty in the CLI-derived command record.
Its matching original tool output at line38 retains the native summary and probe
result; that derivative is saved alongside the unchanged CLI events. Direct native
outputs for every cell contain3 tests and111-versus222, with no outer truncation
notice. Baseline probes also embed another native execution; current probes reuse
the separately executed native tests. Reused output is not a new execution.
Extra baseline cache/filename controls (16 loads versus9 in current) and other
additional work remain in costs; narrower optional work is not superior quality.

Filesystem read observations do not distinguish physical disk from OS caching.
The current relative-cache probe records resolved-path stat before the real read,
not opened-descriptor identity. Other probes also capture real handle identities;
none provides an atomic filesystem snapshot or uninstrumented production proof.
This sequential standard-library fixture does not establish thread safety,
live-edit semantics or deployed configuration behavior.

The original response analyzer gives zero count term in both pairs. Relative
cache's total delta1415 decomposes into first-input4350, later-input−2016 and
output−919; retained binding's9604 into5388,4293 and−77. These are identities,
not attribution to the skill or removable work. Existing instruction consolidation,
generic read-less rules and repeated favorable reruns remain unjustified.

The all-eight better-work/lower-token/faster-time objective remains unfinished.
Keep this mixed result and investigate a distinct evidenced mechanism; do not
promote it to `featured.json` or relabel the unchanged resource as an optimization.

한국어:4회 원본 진단은 실제 구현·파일 읽기와 요구된 대조군을 뒷받침한다.
두 조건 모두 원인을 찾았고 공급 파일의 내용·권한을 보존했다. 적용 합계는
토큰5.40% 증가, 시간18.75% 감소이며 두 지표가 함께 줄어든 과제는 없다.
작성된 관련 과제·조건별1회·실행 순서·추가 검사량과 파일 관찰 한계를 보존한다.
스킬 수정·독립 검증·8개 역할 전체 절감 성과로 승격하지 않는다.
