I’m using the friday skill to trace the release and rollback sequence, then exercise the versioned options functions against the documented contract. I’ll preserve all supplied files and keep the review local.

**Blocked by evidence:** step 4, “rollback overlap,” violates the service contract. Final recovery succeeds, but the entire sequence is unsafe.

Followed root, ops and worker `AGENTS.md` instructions and the friday skill. Exercised the actual versioned `options` functions using `runpy.run_path`, comparing results against `timeout_ms=7500, attempts=4`.

| Step | Consumer/config | Observed timeout_ms / attempts | Contract |
|---|---|---:|---|
| 1 Original | old / legacy | 7500 / 4 | Pass |
| 2 Mixed rollout | old / bridge | 7500 / 4 | Pass |
| 2 Mixed rollout | new / bridge | 7500 / 4 | Pass |
| 3 Old retired, config pruned | new / current | 7500 / 4 | Pass |
| 4 Rollback overlap | new / current | 7500 / 4 | Pass |
| 4 Rollback overlap | old / current | **1000 / 4** | **Fail** |
| 5 Rollback complete | old / legacy | 7500 / 4 | Pass |

Every exercised function preserved its caller-owned config mapping. Unchanged pairings reused their earlier evidence.

The earliest incompatibility occurs when old consumers return while current config remains active. [old.py](project/services/worker/versions/old.py#L2) defaults to 1000 ms because [current.json](project/ops/config/current.json#L1) lacks `timeout_ms`. The call succeeds silently with the wrong timeout. Step 3 is the last compatible state before this failure; step 5 restores correct options but cannot establish safety of work performed during step 4.

**Minimal mitigation:** restore bridge config before reactivating any old consumer, and retain it through the overlap. Both versions returned the required values with bridge config in the actual checks. Confirm configuration application before old consumers become active.

Actual commands run:

- `pwd; rg --files --hidden -g '!.git'`
- Two `python3 - <<'PY'` commands reading instructions, manifest, modules and configs.
- `python3 -B - <<'PY'` exercising all five distinct active consumer/config pairings, comparing exact results and deep-copied inputs, and checking file hashes before/after.

Production config reloading, network timing and process orchestration evidence were not supplied. Local results do not verify those behaviors or recovery of effects from an incorrect timeout.

All supplied files were preserved; no scratch, services, network access, installation, fixes or deployment.
