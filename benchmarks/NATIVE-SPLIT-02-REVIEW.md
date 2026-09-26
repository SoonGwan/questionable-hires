# Native-split02 scoped original review — 2026-09-27

Measured candidate **`6c099d68`**, predecessor **`33530f98`**. The frozen
[protocol](NATIVE-SPLIT-02-PROTOCOL.md), consumer contract and
[original costs](NATIVE-SPLIT-02-COSTS.json) remain unchanged. This review uses
[all six retained original cells](results/native-split-02/), not a rerun.
No full-quality scalar or whole-team efficiency promotion follows.

## Executed outcome and limits

Every original selected suite has13 native methods. It survives each specified
isolated fault. Focused additional regressions pass correct code and reject the
faults through actual assertions about callback invocation. Normal output is
preserved; detection is not a setup/import/timeout error or an empty suite.

| Case / condition | Native counts, in actual execution order | Observed exits in that order |
| --- | --- | --- |
| Single / baseline |13,13,5,5 |0,0,0,1 |
| Single / predecessor |13,13,3,3 |0,0,0,1 |
| Single / candidate |13,13,3,3 |0,0,0,1 |
| Multiple / baseline |13,12,13,12,13,12,13,12 |0,0,0,1,0,1,0,1 |
| Multiple / predecessor |13,13,16,16,13,16,13,16 |0,0,0,1,0,1,0,1 |
| Multiple / candidate |13,13,19,19,13,19,13,19 |0,0,0,1,0,1,0,1 |

For multiple helper runs, the first correct original/focused observations are
reused for the other two faults; reuse is not another execution. Four processes
run in each single case, eight in each multiple case. Native child exits come
from their recorded results, not merely the outer command's exit.

The recording callable produces actual `[1,2,3]` in baseline witnesses and
`[1,0,2]` in helper witnesses, where the consumer requires `[]`. Whole-group
output assertions execute before that failure. A separate locally raising
predicate is converted to a test assertion failure with the actual witness;
`split_at` tests both separator modes. Empty inputs, generator consumption and
ordinary splitting are retained. Baseline multiple checks limits−1/1/2;
other cells rely on the unchanged original ordinary controls and, for single
cases, additional neighboring-function controls. Unequal optional work remains
in costs; method counts are not a quality ranking.

This is specifically the visible consumer's `maxsplit=0` contract. The original
pure predicates cannot expose extra invocations. No general upstream
callback-count promise, production defect or full source-origin claim follows.

## Actual bindings and harness scope

Read the executed command bodies in each cell's `commands.json` alongside its
`native-output.original.txt`; final prose alone is not execution evidence.
Baseline hooks wrap the native runner inside each child process and verify the
loaded package/version, implementation, exported function/code identity, selected
test globals and expected paths. Helper prechecks run inside the actual native
process with copied-import checks and package/implementation/test identities.
Each fault changes only its specified function guard in its independent copy;
original selected test assertions remain unchanged.

Baseline/single intentionally shares `focused_contract.py` under its owned
project-local scratch support directory across the two code variants. Its hook
verifies that exact support path and binding to the variant's package. It is not
inside each variant directory. The frozen criterion says “copy-local ...
consuming-test bindings,” while the visible task asks for actual bindings inside
each native process. Do not invent a stricter hidden directory-placement failure:
retain this layout distinction rather than awarding an unqualified criterion score.
Baseline/multiple and helper probes place their focused modules in the copies.

Five final native captures have no outer truncation marker. Predecessor/multiple
retains the original **391-token cutoff** around a command/copied-import boundary.
Later counts, assertions and binding lines support the scoped outcomes but do not
recover the missing prefix or prove every binding field was captured. No replay
replaces that evidence. That coordinator prints the audit CLI result but does not
forward it as its own process exit; its actual printed child results are the
relevant evidence. Candidate coordinators do forward the CLI exit, which still
must not be confused with the deliberately failing mutant child's exit1.

## Preservation evidence

[Artifact review](results/native-split-02/artifact-review.json) rechecks all six
supplied final inventories, SHA digests and modes against the frozen manifest:
only the six supplied files remain outside Git/installed resources, so no owned
scratch, harness or report remains. Collector snapshots match. Git HEAD matches
each captured initial commit. Installed resources match captured pre-model,
collector and current inventories in both skill conditions; baselines have none.
Before-model and before-collector index bytes/modes match in every cell.

The current workspace index bytes differ from the retained collector copy in all
six cells. That is a later observation, not evidence identifying which action or
actor changed them. Preserve the distinction: original captured index equality
holds, current byte equality does not. No causal blame, transient-action proof or
all-Git-metadata claim follows. Separate pre-model working-file permission
inventories were not available for these historical runs; final modes do not
prove every initial or transient permission bit.

The existing exporter retains original events, answers, commands, supplied source,
usage profiles and digests, with local paths redacted. Full private initial
instructions/session files and binary Git indexes are not published. Pattern
scanning is separate from manual review and does not certify absence of secrets.

## Cost decision and next action

| Sum across two correlated authored cases | Tokens | Seconds |
| --- | ---: | ---: |
| No skill |203,262 |226.248 |
| Predecessor |320,765 |177.971 |
| Candidate |290,769 |173.838 |

Candidate versus no skill: **+43.05% tokens,−23.16% time**. Versus predecessor:
**−9.35% tokens,−2.32% time**, descriptively. Candidate single uses more tokens
than predecessor single; the aggregate is not a uniform improvement. One run per
arm, related fixtures, unequal extra work and shared host/cache prohibit broad
causal or independent-validation claims. All-eight improvement remains unmet.

Both helper multiple paths rerun the original13 methods inside their focused
selection; baseline multiple runs focused-only. This identifies different work,
not an automatic removal authorization: new fixtures/hooks or imports can affect
state and invalidate earlier ordinary observations. Candidate uses quiet mode,
so removing verbose headers is not a demonstrated saving here. Generic batching,
read-less rewrites and forced helpers already have historical mixed results.
Do not repeat these exposed cases until favorable or add another generic rule.

한국어: 기존6회의 원본 검사와 파일 보존을 검토했다. 추가 검사는 실제 콜백
호출을 검출하지만 이전 버전의391토큰 출력 누락, 공유 검사 파일 배치와 평가
문구 차이, 현재 인덱스 바이트 변화 및 초기 작업 파일 모드 한계를 유지한다.
후보는 이전 버전 대비 합계 토큰9.35%·시간2.32% 감소이나 미적용 대비 토큰
43.05% 증가다. 전체8개 역할의 품질·토큰·시간 목표를 달성한 근거는 아니다.
