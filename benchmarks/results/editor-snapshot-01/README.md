# Snapshot QA transfer: routing works, resource results are mixed

[Frozen protocol](../../EDITOR-SNAPSHOT-01-PROTOCOL.md), launch `ff67561`,
Mother-in-law candidate `1cb854d`. One new authored settings-save workload under
two project-support conditions, not two independent domains or an organic
repository holdout. Four fresh serial Astra medium sessions complete: present
skill, absent skill, absent baseline, present baseline. One session per condition
and arm; no retries, transport errors, authoring repairs, exclusions or resource
changes during timing. No concurrent author test workload.

| Project support | Arm | Input + output tokens | CLI seconds | Shell commands |
| --- | --- | ---: | ---: | ---: |
| Present | Baseline | 69,257 | 42.935 | 3 |
| Present | Skill | 56,161 | 45.042 | 3 |
| Present | Skill change | −18.91% | +4.91% | |
| Absent | Baseline | 69,867 | 59.429 | 3 |
| Absent | Skill | 57,362 | 51.533 | 3 |
| Absent | Skill change | −17.90% | −13.29% | |

Cached input counts once; reasoning output is not added again. The absent-support
pair is favorable in both resource metrics, but present-support time is worse.
Do not average away that result or claim a consistent 20–30% gain. n=1, shared
host/cache, fixed order, authored task and different model implementations limit
attribution. There is no old-skill arm here: this does not isolate the wording
change's causal effect. Historical/featured charts are unchanged.

한국어: 새 설정 저장 과제에서도 자료 선택 경로가 동작했다. 기존 테스트 지원이
있으면 관련 transport 자료를 읽지 않았고, 없으면 읽고 필요한 제어 코드를
만들었다. 토큰은 각각 18.91%·17.90% 감소했지만, 시간은 지원이 있는 조건에서
4.91% 증가하고 없는 조건에서 13.29% 감소했다. 네 세션 모두 필요한 결함을
잡았으며, 단일 합성 과제의 두 조건으로 일반 성능이나 일관된 20–30% 절감을
주장하지 않는다.

## What the models actually did

All four preserve production, the original initial-state test and existing
support when supplied. They add exactly two native methods and run the resulting
three-method suite once. Real `Editor.save` is used. Expected nested settings are
independent literals; callback payloads retain their actual references until the
test acknowledges, then the persistence double deep-copies them into its log.
No double eagerly snapshots the argument and thereby hides the production bug.

The normal save stores the expected full payload and becomes clean. The overlap
case starts one save, edits the theme while its actual callback is pending, and
fails at the full pending-payload assertion (`dark` versus the later theme).
Each test safely unwinds to cancellation/cleanup at that failure. Subsequent
stored/current/dirty checkpoints exist but are **not reached in the original
failing case**, as permitted by the frozen request and explicitly reported by
the models. They execute successfully in separate conforming-code replays below.
No browser or external persistence was tested.

Present condition: both reuse `writes()` directly. Skill reads only its entry,
project instructions and supplied files, skipping native transport/probe guides
and assets. Absent condition: skill reads the native guide and transport asset,
then writes a small native `ControlledPersist` using Events and delayed copying;
it does not copy the key-oriented transport. This is a valid adaptation, not
evidence of asset-use efficiency. Both absent arms implement controlled support
inside the test file without installed-skill dependencies.

Every cell still inventories filenames, then reads known files, then executes
native tests: two preparation shell commands and three total. The prior pager's
one-command preparation does **not** transfer. Skill groups these into two outer
tool calls versus baseline's three, but those observations alone do not quantify
which mechanism caused the cost difference. Avoid adding stronger generic
discovery rituals or replaying this exposed task for a nicer score.

Actual work is not identical: absent baseline adds an untouched nested layout
field to expected payloads, uses five-second waits and a try/finally gather;
absent skill uses one-second waits and `addAsyncCleanup`. Present skill adds
live-settings/dirty checks before the intended failing pending-snapshot assertion.
These differences and full original outcomes remain visible; all required
checkpoints are present in every suite.

## Original evidence and separate confirmation

Per-cell exports include commands, original events, answers, changes, final
project files, metadata, source hashes and reviewed tool records. All three
shell outputs and exits per cell match persisted same-session responses exactly
([reconciliation](tool-reconciliation.json)); no missing/duplicate/unmatched
selected tool records. Each original run retains three native identities, one
actual AssertionError, two passes and exit 1. No setup error supplies the failure.
Full private rollout context is local only, not exported.

[Author review](author-review.json) verifies original test AST, source/support
bytes, installed resources and usage. Each unmodified model suite fails on the
original implementation and passes all three methods when only an author-copy
snapshot changes from `dict` to `deepcopy`. This is eight native author runs,
not additional model trials or repaired original evidence. Test-created files
and external I/O are absent; disposable author copies are project-local and
removed. Reproduce with
`python3 -B benchmarks/review_editor_snapshot.py --run benchmarks/local-runs/editor-snapshot-01 --output <new-json>`.

Keep the support-first candidate: the two branch decisions work on a different
workload without losing required regression behavior. Do not claim broad speed
acceptance. The remaining work is real-project transfer and stronger repeated
evidence, not further tuning this same fixture. The all-eight objective remains
unproven.
