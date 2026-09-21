# Landlord boundaries 01 — 2026-09-21

**Reject the compact candidate as a performance upgrade.** Production Landlord
was never replaced. Prior resources and selected source `a062950`, launch
`387e398`; [frozen protocol](LANDLORD-BOUNDARIES-01-PROTOCOL.md),
[all original evidence](results/landlord-boundaries-01/README.md).

| Task | Condition | Total tokens | Wall seconds | Responses / shell commands |
| --- | --- | ---: | ---: | ---: |
| Runtime sharing | Prior | 112,834 | 81.171 | 4 / 5 |
| Runtime sharing | Baseline | 189,635 | 91.444 | 7 / 11 |
| Runtime sharing | Candidate | 144,349 | 87.377 | 5 / 6 |
| Offline inventory | Candidate | 52,714 | 55.532 | 3 / 4 |
| Offline inventory | Baseline | 69,949 | 73.699 | 4 / 3 |
| Offline inventory | Prior | 36,571 | 44.192 | 2 / 2 |

All six meet the five reviewed task/scope criteria. They are static design
reviews, not executed behavior tests. Input includes cached tokens once, output
includes reasoning once. Sums: prior149,405 tokens /125.363s, baseline259,584
/165.143s, candidate197,063 /142.909s. Candidate versus baseline: **−24.09%
tokens /−13.46% time**; versus prior: **+31.90% /+14.00%**. Candidate costs more
than prior on both tasks and metrics. Reporting only baseline would hide that.
Entrypoint words fell318→238; this did not reduce observed whole-task work.

## Reviewed behavior

Runtime: all trace the independently selected skill installation boundary and
explain why a repository-level runtime module would be missing after installation.
They distinguish generic capture mechanics from Python/Node provenance and
environment adapters, audit/receipt unconfirmed-cleanup exceptions versus
Exorcist JSON/CLI125, timeout versus actual child124, interruption and group
cleanup. All compare local duplication with canonical code shipped inside each
skill and trace a concrete maintenance change. No skill requires a sibling runtime
dependency as its recommendation. No helper, installation or native test is run.

Inventory: all find the missing proposed module in the fixed archive selection,
recommend a narrow iterator in the already-shipped installer, and explicitly
allow a separate module if distribution is corrected. They distinguish traversal
from streaming hashes, retained archive bytes, copying, selected-skill policy,
conflicts, modes and deterministic metadata. All notice that installation's
unfiltered source-link preflight must not be replaced by the filtered inventory.
They trace an approved exclusion-policy change through both traversal and copying.

All inventory answers call the unchanged archive member list a constraint more
strongly than the task requires: the contract allows a corrected distribution.
Each nevertheless offers a viable alternative and acknowledges the corrected
separate-module option. This wording issue is retained, not scored as a missing
contract or evidence that all sharing is forbidden.

## Actual work and capture

All three runtime arms first request large whole-source output that is truncated,
then perform focused reads. Candidate also repeats contract/installer reading;
it does not remove the observed recovery work. Baseline has more discovery and
recovery calls. These are observed actions, not causal token attribution.
On the smaller inventory task, prior batches discovery/source reading into one
tool interaction; candidate uses two, baseline three. Baseline's last search of
absent `skills/` exits2. That is a retained discovery error, not a failed native
behavior test. No experiment was rerun, replaced, excluded or interrupted by limits.
No author regression suite ran concurrently.

Original runtime source-output truncation prevents complete matching for prior
CLI items1/2 (stored line18), baseline4/5/6 (line29), and candidate3 (line23).
Do not call those outputs fully reconstructed: the original stored records are
also truncated. Subsequent source reads, correct source-grounded conclusions and
immutable supplied source support review, but do not prove omitted text was seen.
All remaining mapped runtime outputs and all inventory outputs match exactly.
Original events and stored records are both preserved, not replaced by a replay.

All frozen input bytes/modes, resource inventories and HEAD/staged entries match;
no extra project files remain. Pre-session binary-index bytes were unavailable;
staged entries are checked separately. Exact skill bodies appear in initial
messages for all four skill cells. Baseline body matches are unobserved, not proof
of all-context absence. Private initial messages are excluded from public evidence.

## Limits and next decision

Two author-selected design proposals using the author's own real repository,
not organic requests, independent holdouts or production incidents. Fixed serial
order, n=1, shared host/cache, unequal reading and unblinded review prevent a
causal/general advantage claim, including for the cheaper prior skill. Both tasks
share a distribution theme. Keep this candidate and the earlier adverse
[compression result](LANDLORD-COMPACT-01.md) historical; do not retune these tasks
until favorable. No featured-chart promotion or release approval.

Repeated full-source output/recovery is now observed in all three runtime arms.
Any next candidate must address that actual reading workflow while retaining
callers, embedded bootstrap/provenance logic and cleanup semantics, not assume
shorter instructions are enough. Do not add a blanket rule to avoid needed source
inspection or a mandatory extra discovery phase. Whole-eight performance remains
unproven; local release tests do not satisfy it.

한국어: 6개 정적 검토 모두 핵심 요구사항을 충족했지만, 짧은 후보는 기존
스킬보다 토큰31.90%·시간14.00%가 더 들었다. 무스킬 대비 유리한 수치만
선택하지 않고 후보는 채택하지 않는다. 긴 소스 출력 잘림과 재탐색이 실제
비용으로 관찰됐다. 모든 시도와 캡처 한계를 보존하고 대표 그래프는 유지한다.
