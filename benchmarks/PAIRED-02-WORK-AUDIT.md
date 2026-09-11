# Paired 02 work audit: discovery alone does not explain the overhead

Read-only audit of completed command events in the original 18-cell traces from
[paired 02](FAST-PAIRED-02.md). No new model sessions, altered criteria or source
skill edits. Count each `item.completed` command_execution event once. A discovery
command means its command string contains `rg --files` or `ls -la`; a combined
command counts once. This transparent heuristic is not a semantic cost profiler
and does not count every possible discovery operation.

| Case | Baseline commands | Skill commands | Baseline discovery commands | Skill discovery commands |
| --- | ---: | ---: | ---: | ---: |
| history-active | 3 | 3 | 2 | 2 |
| boundary-fix | 4 | 7 | 2 | 2 |
| formatter-review | 3 | 2 | 2 | 1 |
| search-order | 5 | 5 | 2 | 1 |
| search-diagnosis | 4 | 6 | 2 | 2 |
| necessary-state | 4 | 6 | 2 | 2 |
| persistence-test | 4 | 4 | 2 | 2 |
| rolling-schema | 4 | 5 | 2 | 4 |
| search-protected | 4 | 5 | 2 | 2 |
| Total | 35 | 43 | 18 | 18 |

The bundle has eight additional shell-command events, but the same number of
commands containing these discovery forms. This does not imply equivalent
discovery content, nor exclude overhead from skill loading or repeated reads.
It rules out using this count to claim excess discovery is the sole demonstrated
cause. Patch events are separate and not included in this table.

## Concrete differences worth preserving

Receipt produces identical code/test changes and equivalent failing-before /
passing-after assertions. Baseline combines the final test, diff check and diff
stat in one command; skill runs final tests, whitespace check and focused diff
in three commands. Skill also reads its entrypoint in an extra command and reads
irrelevant initial commit metadata. A compact verification collection step is a
plausible opportunity, but no per-command model token/time accounting is available
to assign its benefit. Combining shell commands must not hide a test's own status.

Friday repeats file/inventory inspection and reads initial commit metadata twice
(log, then show --stat) despite having the release/SQL/reader files. Its runtime
also checks an update and insertion that baseline does not. Remove neither those
data checks nor required release reasoning merely to match baseline cost.

Exorcist reads its entire small process-runner source and reference, then runs a
hard-bounded experiment; baseline lacks hard containment and gives a narrower
explanation. Source review may be justified for trust, not automatically wasted.
The run does not establish why the agent chose that review or which instruction
caused it. Do not ban helper inspection to force a favorable score.

Hostage and broken-search skill runs each have an unknown rejected patch target.
Their long times cannot be decomposed into useful work and retry overhead from
the available event-level data. Final correct files do not explain the rejection.
Persistence skill uses the same number of commands, fewer tokens and more time,
with more explicit import verification and child deadlines. Command count is not
a reliable standalone optimization objective.

## Next action, not another benchmark or blanket rule

Do not add universal "fewer calls" or "never inspect source" instructions to all
eight skills. The evidence supports examining Receipt's delivery/verification
collection and Friday's unrelated history collection separately, while preserving
actual test statuses and migration-data checks. Any resulting candidate needs a
concrete task-work reduction mechanism, not just another instruction saying to be
efficient. The full bundle remains unaccepted; no new performance claim follows
from this trace audit.
