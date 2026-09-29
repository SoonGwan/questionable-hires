# Compact audit delivery modes01 review — 2026-09-28

Previous resource **`145d5c3d`**, isolated candidate/execution **`fa158c22`**.
[Protocol](COMPACT-AUDIT-MODES-01-PROTOCOL.md),
[original costs](results/compact-audit-modes-01/comparison.json),
[response counters](results/compact-audit-modes-01/response-cost.json),
[arithmetic](results/compact-audit-modes-01/metrics.json).

**Decline adoption.** The compact entry reduces cost in the proposal task, but the
required-verification task increases both tokens and elapsed time. The frozen gate
requires both pairs to improve. No ordinary skill, personal installation, featured
chart or hosted download changes; do not repeat this unchanged candidate.

| Task | Previous tokens | Candidate tokens | Change | Previous CLI s | Candidate CLI s | Change | Responses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Proposal only |127,506|92,690|−27.31%|81.340|80.953|−0.48%|5→4|
| Verified assertions |124,964|132,856|+6.32%|100.756|155.802|+54.63%|5→6|
| Sum |252,470|225,546|−10.66%|182.096|236.755|+30.02%|10→10|

Input includes cache once, plus output. All four fresh Astra/medium sessions finish
within their360-second cap without scheduler retry, replacement or timeout. Their
internal failed attempts remain charged. No author test/replay runs concurrently.
The candidate entry is2,626 bytes versus5,781; frontmatter and all non-entry
resources are unchanged. Instruction bytes are not measured token savings.

## Original native observations

Both unchanged, previously exposed tasks use cachetools5.5.2 and the same four
LRU faults against the same two actual native tests. All four sessions report:

| Independent fault | Plain native test | Weighted native test |
| --- | --- | --- |
| Omit read recency | Detected: behavioral KeyError at test line26 | Survives |
| Omit overwrite recency | Survives | Survives |
| Evict most recently used | Detected: behavioral KeyError at line19 | Survives |
| Ignore getsizeof | Survives | Detected: AssertionError3 !=1 at line48 |

The KeyErrors occur in reached native test behavior, not during import. Native
unittest's ERROR label alone does not make them invalid setup failures. Mutation
edits are confined to LRUCache; other classes and original source/tests are preserved.
There is a mutation difference: previous verified records membership before the
base write; the other three inspect the order mapping after the write. These expose
the intended missing-refresh fault with the supplied stable-size witnesses; they
are not established equivalent for arbitrary size-changing eviction/reinsertion.

Previous proposal uses the existing native batch helper: two actual normal runs
reused across eight mutant runs, **10 native processes**. Its16 printed check records
include six explicit baseline observation references; these are not six additional
executions. Whole-project guarding and copied test/class bindings are checked.
Its first source read tries nonexistent `cachetools/lru.py` and exits1, then reads
the actual module. That is a source-discovery error, not native detection.

Candidate proposal writes a custom harness with **10 native processes**, separately
invoking both selected tests in each of five copies. PYTHONVERBOSE output verifies
actual copied package and test imports in those processes. It avoids reading the
optional helper guide and prints less native output. Both proposal sessions respect
the requested mode: stronger assertions are proposed, not claimed executed. The
candidate explicitly labels its concrete overwrite/weighted-read proposals unrun.
Its child native calls have no individual timeout; the frozen session cap remains.
Different helper use, source reads and output lengths make this unequal work, not
proof that the shorter entry caused a saving.

Previous verified uses a custom harness with **13 native processes**: five suites
containing both original tests, plus eight stronger correct/fault checks. Same-process
hooks verify copied test/module paths and native test globals bound to copied LRUCache.
The stronger overwrite method exercises both unweighted and weighted subtests;
read/MRU use weighted witnesses and the size callback has a direct size assertion.
All four stronger checks pass correct code and fail their intended faults.

Candidate verified reads the native batch guide but writes its own harness. Its
first baseline executes one passing native test, then its wrapper fails because
sitecustomize was not loaded: the copy root was absent from the startup import path.
It does not count that attempt as verified. It sets child PYTHONPATH to the copy
and repeats the baseline within the same model session. The corrected program runs
10 original checks plus eight stronger checks: **19 native processes total**, including
the first attempt. All cost and the original failure are retained. This is neither a
scheduler retry nor evidence that the first native test itself failed.

The corrected candidate hook checks copied module/test paths, native class aliases,
LRUCacheTest.Cache and the selected method's actual globals. Stronger weighted-read,
weighted-MRU and size-callback witnesses distinguish correct/faulty code. Its shared
overwrite witness is **unweighted only**, explicitly mapped to both surviving original
overwrite gaps in the final answer; the task permits a shared witness when coverage
is established. It does not separately execute the weighted-overwrite regression
that previous verified executes. Keep this narrower observed coverage visible;
do not claim identical checks or unrestricted quality parity. Both verified programs
bound child native calls at30 seconds. Their stronger failures are intended assertions,
not setup failures after the candidate's path correction.

## Preservation, capture and limits

[Artifact checks](results/compact-audit-modes-01/artifact-review.json) find no final
project changes or extra files in any cell; installed resources, HEAD and captured
pre-collector index bytes/modes remain unchanged. Owned scratch is removed.
[Exact frozen-input checks](results/compact-audit-modes-01/frozen-identity-review.json)
confirm every task file and installed condition snapshot. These boundary observations
do not prove absence of all transient changes.

[Output pairing](results/compact-audit-modes-01/capture-review.json) covers21 commands:
18 exact CLI/original matches and three CLI suffixes. Missing prefixes for candidate
proposal, candidate verified's failed first harness and previous verified are saved
from the same original paired records. No unpaired output, exit mismatch or truncation
marker is observed in this review; no replay repairs model evidence. Original records,
line hashes, events, final answers and usage profiles remain accessible under each arm.
The recovered previous verified unittest output retains its original trailing space
after a subtest progress line. Exact entry bodies are observed in tool output in all four; initial exposure remains
unobserved, not proven absent. Private initial instruction text is not published.

[Preflight](results/compact-audit-modes-01/preflight.json) uses20 actual native
invocations:12 selected-test runs, two full15-test correct/equivalent suites and
six behavioral witnesses. Public imports and intended failures are checked using
an explicit repository-local scratch parent. Four synthetic scheduler/resource
controls pass in checkout and a Git-free file copy containing the actual fixture;
candidate skill validation also passes. These are author controls before models,
not additional model evidence or independent holdouts.

One observation per condition/task, exposed authored cases, shared source/faults,
shared host/cache, context variation and unequal checks limit interpretation. There
is no no-skill control or general causal claim. The old favorable lean Con Artist
pair remains historical; the old full bundle's Hostage scope failure also remains.
Both README capability descriptions, frozen featured data and integration07 stay
unchanged. Whole-eight quality/lower-token/faster-time improvement remains unmet.

한국어: 축약 후보는 제안 과제에서 토큰27.31%·시간0.48% 감소했지만, 실제 검증
과제에서는 토큰6.32%·시간54.63% 증가해 채택하지 않는다. 검증 후보의 첫 경로
확인 실패와 재실행까지 포함하면 네이티브 실행은 기존13회→후보19회다. 기존은
덮어쓰기의 가중/비가중 검사를 모두 했고 후보는 공유 비가중 검사만 실행했으므로
검사량도 같다고 볼 수 없다. 합계 토큰10.66% 감소만 강조하지 않으며 시간은30.02%
증가했다. 네 원본 실행·불리한 결과·출력 복구 근거를 보존하고 설치본과 공개 웹은 유지한다.
