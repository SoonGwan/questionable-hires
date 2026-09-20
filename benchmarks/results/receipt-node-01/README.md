# Native Node comparison pilot: faster here, substantially more tokens

2026-09-21. Launch `0cddd83`, prior Receipt `310d483`, Node-enabled Receipt
`8fa20dd`. Two related **authored synthetic** tasks, three conditions, n=1 per
condition; GPT-6 Astra medium, serial shared host/cache, 360-second cell limit.
[Frozen protocol](../../RECEIPT-NODE-01-PROTOCOL.md), [final manifest](run.json),
[reviewed comparison](comparison.json). All six scheduled attempts are retained;
no retry, timeout, account-limit stop, exclusion or author native replay.

## Outcomes and costs

All six meet the five explicit criteria: same four native tests, actual before
failure/after success, correct mechanism, revision/working-tree and native-process
module identity, preservation and cleanup. This is unblinded author review of
commands, original outputs and retained files—not a score inferred from completion.

| Task | Condition | Input + output tokens | Seconds | Recorded responses |
| --- | --- | ---: | ---: | ---: |
| ESM, committed fix | baseline | 67,925 | 60.264 | 4 |
| ESM, committed fix | original | 72,951 | 75.147 | 4 |
| ESM, committed fix | current | 98,451 | 44.920 | 5 |
| CommonJS, working fix | baseline | 68,347 | 66.886 | 4 |
| CommonJS, working fix | original | 74,531 | 79.820 | 4 |
| CommonJS, working fix | current | 112,390 | 48.680 | 5 |
| Both tasks, sum | baseline | 136,272 | 127.150 | 8 |
| Both tasks, sum | original | 147,482 | 154.967 | 8 |
| Both tasks, sum | current | 210,841 | 93.600 | 10 |

Current versus baseline: **+54.72% tokens / −26.39% elapsed time**. Versus original:
**+42.96% tokens / −39.60% time**. These ratios of two-task sums are descriptive,
not averages of task ratios, confidence intervals, causal effects or broad gains.
Cache is included once in input; reasoning is not added again to output. The goal
of better work at similar/lower token and time cost remains unmet. No dollar claim.

## What was actually verified

In each original native comparison, the earlier decoder passes split header,
coalesced frames and empty-frame/input controls, but fails the split binary payload
assertion: `[]` instead of `['00ff0d0a']`. The unchanged current four tests all pass
on the fixed implementation. The mechanism is premature consumption of the length
header, not a setup failure. Native statuses are respectively 1 and 0; no skipped
tests. Loaded module origins/PIDs lie in corresponding local copies. ESM references
two full commits; CommonJS retains the original HEAD and identifies unstaged bytes
by SHA-256. Each final answer distinguishes tested behavior from broader assurance.

Current uses the installed helper in both tasks; the other four attempts implement
native copying/execution/cleanup themselves. Current's load records match the tests'
already supplied `ACTUAL_MODULE` records. Helper adoption is observed, not a success
criterion. Baselines and original also provide the required evidence.

All four supplied files per cell match frozen final fixture bytes/modes (0644),
with no extra exported project files or scratch. HEAD, retained pre-collection staged
entries and installed resources match initial identities. Original execution records
also contain matching whole-tree interval snapshots and cleanup. The independent
index check compares entries, not an unavailable pre-session binary index snapshot;
do not expand this into protection against concurrent/restored changes.

## Capture and exposure

Four final native CLI outputs omit a prefix but match the suffix of their original
stored tool response. No native rerun supplies the missing identity evidence:

| Cell | CLI item | Original stored line | CLI / original normalized characters |
| --- | --- | ---: | ---: |
| ESM baseline | item_3 | 28 | 3,127 / 3,647 |
| ESM original | item_4 | 31 | 3,324 / 4,039 |
| CommonJS original | item_4 | 31 | 4,680 / 5,366 |
| CommonJS baseline | item_4 | 30 | 3,124 / 3,444 |

Both current captures match original outputs completely. Native statuses match in
every pair; tool call/output IDs reconcile without missing/duplicate records.
See each cell's `tool-records.json`, `commands.json` and `usage-profile.json`.
Original private rollouts are retained locally, **not exported**. Evidence scan passes.

All four skill entrypoints appear exactly in their recorded initial messages and
later tool output. Baseline matching against current entry text is unobserved, not
proof of total skill absence. `skill-exposure.json` exposes hashes/locations only,
not private initial instructions. Condition-level `run.json` files are preparation
snapshots; the top-level final manifest records all six completions.

## What to improve next, without rewriting these results

Current removes handwritten comparison orchestration but adds guide/reference and
implementation inspection plus an extra recorded response in both tasks. CommonJS
also reads the preservation-only helper and uses `--pretty`; ESM uses compact JSON.
These are observed costs, not proof every inspection was unnecessary or a causal
token attribution. Do not add mandatory extra checks or repeat these exposed cases
until a favorable result appears. Investigate why routine invocation needed those
compatibility/preservation reads before proposing a narrower support interface.

Containment differs: current supplies process-group cleanup; original uses native
child timeouts; baseline generated comparisons have no individual child timeout
(all six sessions have the external cell limit). CommonJS baseline removes child
`NODE_OPTIONS`; this is not evidence for compatibility with custom startup setups.
The helper is retained as verified functionality, **not a token-efficiency release**.
Featured charts and existing benchmark resources remain unchanged.

한국어: 두 합성 과제 모두 세 조건이 요구된 검증을 충족했다. 현재 스킬은 직접
비교 코드를 작성하는 작업을 대신했지만, 두 과제 합계 기준 무스킬보다 시간은
26.39% 적고 총 토큰은 54.72% 많았다. 이전 스킬 대비도 시간 감소·토큰 증가다.
단일 실행·공유 환경의 관측이며 일반 성능 향상은 입증되지 않았다. 누락된 화면
출력은 재실행이 아닌 원본 기록으로 확인했고, 모든 결과와 한계를 보존한다.
