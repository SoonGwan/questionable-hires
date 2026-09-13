# Display-retention development checkpoint 01

Resource/launch `0e80f9b`. Three new authored tasks, six fresh serial Astra medium
sessions, one repeat per arm. These capability-selected tasks are not organic,
independent holdouts or an all-eight benchmark.

| Arm | Input + output tokens | Process seconds | Reviewed targets |
| --- | ---: | ---: | ---: |
| Baseline | 233,865 | 231.252 | 3/3 |
| Skill | 230,174 | 109.226 | 3/3 |

Recorded aggregate skill change: **−1.58% tokens / −52.77% time**. Both find two
faults and avoid a false positive on one clean case. The skill invokes its new
retention mode for all three tasks. All six cells completed, no exclusions.

The clean case increases skill tokens by 34.35%; do not hide it behind favorable
fault-case results. Baseline additionally uses dictionary/identity/peer checks and
long custom rerun commands; skill additionally runs default cases and depends on
its installed helper. Shared host/cache and n=1 limit inference. No causal,
universal or 20–30% overall efficiency claim follows from these observations.

- [Frozen protocol](../../MOTHER-RETENTION-MODEL-01-PROTOCOL.md)
- [Native per-cell review and reconciliation](../../MOTHER-RETENTION-MODEL-01-REVIEW.md)
- [Schedule](run.json), [all raw metadata](summary.json)

Each cell includes redacted full events/commands, answer, final project files,
diffs, metadata and provenance hashes for raw local originals. All source files
and installed resources were preserved. Native evidence was not replaced by
author replay. Historical/featured graphs retain their original datasets.
