# Personal Mac installation sync — 2026-09-28

Source `2db6852c`; local installation delivery, not a model-efficiency result or
public/hosted release. The owner's existing `.agents/skills` copies differed from
the repository in three hires: Con Artist, Necromancer and Receipt. Five other
hires already matched. Installed copies do not follow source commits automatically.

Eleven differing installed files match historical Git blobs for their same paths;
there are no additional regular resources or mode differences in those hires.
Receipt is also missing assertions.py. This establishes source history, not why
an older copy was retained. The entire old folders were moved to a new backup
outside skill discovery before replacement, preserving rollback material.

The existing installer first stages the three current copies. Inventories and five
executable CLI help checks pass before replacement. Old live inventories are
rechecked; only these three folders move. Any replacement/verification error in
the recorded control attempts restoration from the old folders, without deleting
an unexpectedly changed live copy. The successful path did not exercise rollback.

After replacement, the existing read-only installer comparison finds **all eight
hires/52 resources matching current source bytes and file modes**. Old backup
inventories still match. Generated Python caches are excluded from these resource
comparisons. No host discovery/restart, remote installer, plugin registration or
cross-platform execution is implied by matching local files.

Actual installed Receipt behavior is verified on both reused SQLite fixtures:

| Installed resource / fixture | Result |
| --- | --- |
| Before sync, both recipes requesting assertion observation | Recipe rejected because this installed version does not accept observe_assertions; no native tests launched. |
| After sync, complete application fix | Native before1/after0; five tests per phase,14 complete v3 argument pairs per phase. |
| After sync, partial application fix | Native before1/after1; five tests per phase,14 complete v3 argument pairs per phase. |

These are four actual native processes after sync. The current installed helper
verifies copied imports in those processes, preserves fixture source inventory
and removes comparison copies. Both after checks retain the real failure/success
distinction; the observer does not turn the incomplete application fix into a pass.
The before recipe errors remain in the evidence. No model tokens/time were measured.

[Summary](../benchmarks/results/personal-install-sync-20260928/summary.json),
[before](../benchmarks/results/personal-install-sync-20260928/before-native.json),
[after](../benchmarks/results/personal-install-sync-20260928/after-native.json),
[inventories/history](../benchmarks/results/personal-install-sync-20260928/manifest.json)
and the [executed one-off control](../benchmarks/results/personal-install-sync-20260928/control.py)
retain source identities and scoped evidence. Paths are redacted in public artifacts.
This control is an operation record, not a new general-purpose upgrade command.

The local backup is under
`~/.agents/skill-backups/questionable-hires/20260928-personal-sync-2db6852c/old/`.
It contains only the three previous installed skill directories. Restore a chosen
old copy only after preserving the current copy and any later edits; do not merge
the old and current resource sets. The five already matching installs were not moved.

한국어: 실제 Mac 설치본3개를 현재 기본 리소스로 갱신했다. 기존3개 폴더는
검색 경로 밖에 백업했고 나머지5개는 그대로다. 전체8개/52개 리소스가 소스와
파일·권한이 일치하며, 실제 설치 경로의 Receipt가 두 SQLite 과제를 정확히
구분하고 v3 관찰을 기록한다. 변경 전 옵션 거부도 보존한다. 모델 성능 향상이나
공개 배포·호스트 검색·다른 운영체제 검증으로 주장하지 않는다.
