I’ll read the release plan and applicable instructions, then run the versioned options functions for each active pairing and check their values against the service contract. I’ll preserve all supplied files and keep the review local.

The release first violates compatibility at **step 4, “rollback overlap.”** The old consumer receives `current.json` and silently returns a 1,000 ms timeout instead of the required 7,500 ms. Step 5 restores compatibility, but the complete sequence is unsafe.

Followed `AGENTS.md`, `ops/AGENTS.md`, and `services/worker/AGENTS.md`: repository-relative paths, listed phase order, exact contract values, and unchanged caller-owned mappings.

| Step | Active consumer | Config | Returned `timeout_ms` | Returned `attempts` | Contract |
|---|---|---|---:|---:|---|
| 1 Original | old | legacy.json | 7500 | 4 | Pass |
| 2 Mixed rollout | old | bridge.json | 7500 | 4 | Pass |
| 2 Mixed rollout | new | bridge.json | 7500 | 4 | Pass |
| 3 Old retired/config pruned | new | current.json | 7500 | 4 | Pass |
| 4 Rollback overlap | new | current.json | 7500 | 4 | Pass |
| 4 Rollback overlap | old | current.json | **1000** | 4 | **Fail** |
| 5 Rollback complete | old | legacy.json | 7500 | 4 | Pass |

All seven calls completed successfully and left their input mappings unchanged. Successful calls therefore do not establish compatibility.

`old.py` reads `timeout_ms`, defaulting to `1000` when absent. `current.json` contains only `timeout_seconds` and `attempts`.

**Minimal mitigation:** restore `bridge.json` before reactivating old consumers and retain it throughout rollback overlap. Additional actual calls confirmed both versions return `{'timeout_ms': 7500, 'attempts': 4}` with that configuration, without modifying it.

Actual commands executed:

- `pwd; rg --files --hidden -g '!\.git/**'`
- `python3 - <<'PY' … PY` — read instructions, manifest, configurations, and version sources using `pathlib`.
- `python3 -B - <<'PY' … PY` — loaded both actual modules with `runpy.run_path`, invoked `options(config)` for every active pairing in manifest order, compared results against the contract and inputs against deep copies, then exercised the mitigation. SHA-256 file snapshots before and after matched.

Production configuration reloading, network timing, and process orchestration evidence are unavailable. These local results cannot establish that production switches configuration before old consumers become active.

All supplied files were preserved; no scratch files, services, network access, installations, fixes, or deployments were used.
